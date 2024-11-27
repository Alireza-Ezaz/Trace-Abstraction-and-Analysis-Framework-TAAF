# gnn_link_prediction.py

import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.utils import from_networkx, negative_sampling
import torch_geometric.transforms as T
from torch_geometric.nn import GCNConv
import pandas as pd
import networkx as nx


# Step 1: Read the triplets CSV and construct the graph
def load_graph_from_csv(triplets_csv):
    df = pd.read_csv(triplets_csv)

    # Create mappings for nodes
    node_ids = pd.unique(df[['source', 'target']].values.ravel('K'))
    node_id_mapping = {node_id: idx for idx, node_id in enumerate(node_ids)}
    num_nodes = len(node_ids)

    # Build the NetworkX graph
    G = nx.Graph()
    for _, row in df.iterrows():
        src = node_id_mapping[row['source']]
        dst = node_id_mapping[row['target']]
        G.add_edge(src, dst)

    # Add node features (optional)
    for node in G.nodes():
        G.nodes[node]['x'] = [1.0]  # You can add real features if available

    return G, node_id_mapping


# Step 2: Convert NetworkX graph to PyTorch Geometric Data
def convert_to_pyg_data(G):
    data = from_networkx(G)
    data.edge_index = data.edge_index.long()
    data.num_nodes = G.number_of_nodes()

    return data


# Step 3: Prepare data for link prediction
def prepare_data_for_link_prediction(data):
    # Positive edges (existing edges)
    pos_edge_index = data.edge_index

    # Negative edges (non-existing edges)
    neg_edge_index = negative_sampling(
        edge_index=pos_edge_index,
        num_nodes=data.num_nodes,
        num_neg_samples=pos_edge_index.size(1)
    )

    data.pos_edge_index = pos_edge_index
    data.neg_edge_index = neg_edge_index

    return data


# Step 4: Define the GNN model for link prediction
class LinkPredictor(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels):
        super(LinkPredictor, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)

    def encode(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        return x

    def decode(self, z, edge_index):
        # Inner product between node embeddings
        return (z[edge_index[0]] * z[edge_index[1]]).sum(dim=1)

    def decode_all(self, z):
        prob_adj = z @ z.t()
        return (prob_adj > 0).float()


# Step 5: Train the model
def train(model, data, optimizer):
    model.train()
    optimizer.zero_grad()
    z = model.encode(data.x.float(), data.edge_index)

    # Positive edges
    pos_pred = model.decode(z, data.pos_edge_index)
    pos_label = torch.ones(pos_pred.size(0), device=pos_pred.device)

    # Negative edges
    neg_pred = model.decode(z, data.neg_edge_index)
    neg_label = torch.zeros(neg_pred.size(0), device=neg_pred.device)

    # Combine predictions and labels
    pred = torch.cat([pos_pred, neg_pred], dim=0)
    label = torch.cat([pos_label, neg_label], dim=0)

    loss = F.binary_cross_entropy_with_logits(pred, label)
    loss.backward()
    optimizer.step()
    return loss.item()


# Step 6: Test the model
def test(model, data):
    model.eval()
    with torch.no_grad():
        z = model.encode(data.x.float(), data.edge_index)

        # Positive edges
        pos_pred = model.decode(z, data.pos_edge_index).sigmoid()
        pos_label = torch.ones(pos_pred.size(0), device=pos_pred.device)

        # Negative edges
        neg_pred = model.decode(z, data.neg_edge_index).sigmoid()
        neg_label = torch.zeros(neg_pred.size(0), device=neg_pred.device)

        # Combine predictions and labels
        pred = torch.cat([pos_pred, neg_pred], dim=0)
        label = torch.cat([pos_label, neg_label], dim=0)

        # Compute accuracy
        pred_binary = (pred > 0.5).float()
        accuracy = (pred_binary == label).sum().item() / label.size(0)
    return accuracy


# Step 7: Use the model to answer "Is X connected to Y"
def predict_link(model, data, node_id_mapping, node_id_x, node_id_y):
    model.eval()
    with torch.no_grad():
        z = model.encode(data.x.float(), data.edge_index)
        idx_x = node_id_mapping.get(node_id_x)
        idx_y = node_id_mapping.get(node_id_y)
        if idx_x is None or idx_y is None:
            print(f"One or both nodes not found in the graph.")
            return False
        pred = model.decode(z, torch.tensor([[idx_x], [idx_y]], dtype=torch.long).to(z.device)).sigmoid()
        return pred.item() > 0.5


# Main function
def main():
    triplets_csv = '../output/knowledge_graph_output/kg_triplets.csv'
    G, node_id_mapping = load_graph_from_csv(triplets_csv)

    data = convert_to_pyg_data(G)
    data = prepare_data_for_link_prediction(data)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = LinkPredictor(in_channels=1, hidden_channels=16).to(device)
    data = data.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    # Training loop
    for epoch in range(100):
        loss = train(model, data, optimizer)
        if epoch % 10 == 0:
            accuracy = test(model, data)
            print(f'Epoch {epoch}, Loss: {loss:.4f}, Accuracy: {accuracy:.4f}')

    # Example query: Is X connected to Y
    node_id_x = 'T_5123'  # Replace with node X
    node_id_y = 'CPU_0'  # Replace with node Y

    connected = predict_link(model, data, node_id_mapping, node_id_x, node_id_y)
    print(f"Is '{node_id_x}' connected to '{node_id_y}'? {'True' if connected else 'False'}")


if __name__ == "__main__":
    main()
