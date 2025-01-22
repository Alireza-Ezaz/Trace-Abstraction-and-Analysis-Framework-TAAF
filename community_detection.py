#!/usr/bin/env python3

"""
local_preprocess.py

1) Load 'knowledge_graph.json'
2) Build a NetworkX graph
3) Perform Louvain community detection
4) Visualize communities via matplotlib
5) Save 'knowledge_graph_with_communities.json' with 'communityId' appended to each node
"""

import json
import networkx as nx
import community  # python-louvain
import matplotlib.pyplot as plt

def main():
    input_file = "output/knowledge_graph_output/knowledge_graph.json"
    output_file = "knowledge_graph_with_communities.json"

    print(f"Loading raw knowledge graph from {input_file} ...")
    with open(input_file, 'r') as f:
        data = json.load(f)

    nodes = data['nodes']
    links = data['links']

    # 1. Build a NetworkX graph (undirected) from nodes & links
    G = nx.Graph()

    # Add nodes
    for node in nodes:
        node_id = node['id']
        # We store the entire node dict as an attribute if we want
        # or keep it simple
        G.add_node(node_id, label=node.get('label', ''), entity=node.get('entity', ''))

    # Add edges
    for link in links:
        source = link['source']
        target = link['target']
        weight = link.get('weight', 1)
        relationship = link['relationship']
        G.add_edge(source, target, weight=weight, relationship=relationship)

    # 2. Perform Louvain community detection
    print("Performing Louvain community detection...")
    partition = community.best_partition(G, weight='weight')  # dict: node -> communityId

    # 3. Insert communityId back into the node dictionary
    node_map = {n['id']: n for n in nodes}
    for node_id, comm_id in partition.items():
        node_map[node_id]['communityId'] = comm_id

    # 4. Visualize communities
    print("Visualizing the graph with communities (matplotlib)...")
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, weight='weight', seed=42)  # layout
    # Color nodes by community
    communities = list(partition.values())
    unique_comms = list(set(communities))
    # Map each community to a color index
    # We'll just pick from a standard colormap; for large graphs, you might want a bigger palette
    comm_colors = {}
    for idx, c in enumerate(unique_comms):
        comm_colors[c] = idx

    node_colors = [comm_colors[partition[n]] for n in G.nodes()]

    # Draw nodes
    nx.draw_networkx_nodes(G, pos,
                           node_color=node_colors,
                           cmap=plt.cm.get_cmap('rainbow', len(unique_comms)),
                           node_size=150)
    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    # Optionally draw labels, but can be cluttered if large
    # nx.draw_networkx_labels(G, pos, font_size=6)

    plt.title("Graph Colored by Louvain Communities")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("communities_visual.png", dpi=150)
    plt.show()
    print("Saved a figure as 'communities_visual.png'.")

    # 5. Save updated graph JSON
    print(f"Writing updated knowledge graph to {output_file} ...")
    with open(output_file, 'w') as out:
        json.dump({
            "nodes": nodes,
            "links": links
        }, out, indent=2)

    print("All done. The new file (with 'communityId') is ready.")

if __name__ == "__main__":
    main()
