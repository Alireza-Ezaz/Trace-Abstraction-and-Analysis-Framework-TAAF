import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
from networkx.readwrite import json_graph

# Utility functions
def parse_contents(contents_str):
    contents_dict = {}
    for pair in contents_str.split(','):
        key_value = pair.strip().split('=')
        if len(key_value) == 2:
            key, value = key_value
            contents_dict[key.strip()] = value.strip()
    return contents_dict

def add_node_if_not_exists(G, node_id, entity_type, label):
    if node_id and not G.has_node(node_id):
        G.add_node(node_id, entity=entity_type, label=label)

def add_edge_with_weight(G, u, v, key, relationship, **kwargs):
    if u and v:
        if G.has_edge(u, v, key=key):
            G[u][v][key]['weight'] += 1
        else:
            G.add_edge(u, v, key=key, relationship=relationship, weight=1, **kwargs)

# Handler functions
def handle_sched_waking(row, G):
    contents = parse_contents(row['Contents'])
    comm = contents.get('comm', 'Unknown')
    tid = row['TID']
    target_cpu = contents.get('target_cpu')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    cpu_node = f"CPU_{target_cpu}" if target_cpu else None
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"{comm} ({tid_node})")
        if cpu_node:
            add_node_if_not_exists(G, cpu_node, 'CPU', f"CPU {target_cpu}")
            edge_key = f"{tid_node}_to_{cpu_node}_scheduled_to_wake_on"
            add_edge_with_weight(G, tid_node, cpu_node, edge_key, 'scheduled_to_wake_on')

def handle_sched_wakeup(row, G):
    contents = parse_contents(row['Contents'])
    comm = contents.get('comm', 'Unknown')
    tid = row['TID']
    target_cpu = contents.get('target_cpu')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    cpu_node = f"CPU_{target_cpu}" if target_cpu else None
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"{comm} ({tid_node})")
        if cpu_node:
            add_node_if_not_exists(G, cpu_node, 'CPU', f"CPU {target_cpu}")
            edge_key = f"{tid_node}_to_{cpu_node}_wake_up"
            add_edge_with_weight(G, tid_node, cpu_node, edge_key, 'wake_up')

def handle_sched_switch(row, G):
    contents = parse_contents(row['Contents'])
    prev_comm = contents.get('prev_comm', 'Unknown')
    prev_tid = contents.get('prev_tid')
    next_comm = contents.get('next_comm', 'Unknown')
    next_tid = contents.get('next_tid')
    cpu_id = row['CPU']
    prev_tid_node = f"T_{int(prev_tid)}" if prev_tid and prev_tid.isdigit() else None
    next_tid_node = f"T_{int(next_tid)}" if next_tid and next_tid.isdigit() else None
    cpu_node = f"CPU_{cpu_id}"
    add_node_if_not_exists(G, cpu_node, 'CPU', f"CPU {cpu_id}")
    if prev_tid_node:
        add_node_if_not_exists(G, prev_tid_node, 'Thread', f"{prev_comm} ({prev_tid_node})")
        edge_key_prev = f"{prev_tid_node}_to_{cpu_node}_switch_out"
        add_edge_with_weight(G, prev_tid_node, cpu_node, edge_key_prev, 'switched_out')
    if next_tid_node:
        add_node_if_not_exists(G, next_tid_node, 'Thread', f"{next_comm} ({next_tid_node})")
        edge_key_next = f"{cpu_node}_to_{next_tid_node}_switch_in"
        add_edge_with_weight(G, cpu_node, next_tid_node, edge_key_next, 'switched_in')

def handle_syscall_entry_ioctl(row, G):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    fd = contents.get('fd', 'Unknown')
    cmd = contents.get('cmd', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    file_node = f"File_{fd}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_node_if_not_exists(G, file_node, 'File', f"FD={fd}")
        edge_key = f"{tid_node}_to_{file_node}_ioctl"
        add_edge_with_weight(G, tid_node, file_node, edge_key, 'ioctl', cmd=cmd)

def handle_syscall_entry_splice(row, G):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    fd_in = contents.get('fd_in', 'Unknown')
    fd_out = contents.get('fd_out', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    file_node_in = f"File_{fd_in}"
    file_node_out = f"File_{fd_out}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_node_if_not_exists(G, file_node_in, 'File', f"Input FD: {fd_in}")
        add_node_if_not_exists(G, file_node_out, 'File', f"Output FD: {fd_out}")
        edge_key_in = f"{tid_node}_to_{file_node_in}_splice_in"
        edge_key_out = f"{tid_node}_to_{file_node_out}_splice_out"
        add_edge_with_weight(G, tid_node, file_node_in, edge_key_in, "splice_in")
        add_edge_with_weight(G, tid_node, file_node_out, edge_key_out, "splice_out")

def handle_syscall_entry_sync_file_range(row, G):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    fd = contents.get('fd', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    file_node = f"File_{fd}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_node_if_not_exists(G, file_node, 'File', f"FD={fd}")
        edge_key = f"{tid_node}_to_{file_node}_sync_file"
        add_edge_with_weight(G, tid_node, file_node, edge_key, "sync_file")

def handle_sched_stat_runtime(row, G):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    cpu_id = row['CPU']
    runtime = contents.get('runtime', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    cpu_node = f"CPU_{cpu_id}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_node_if_not_exists(G, cpu_node, 'CPU', f"CPU {cpu_id}")
        edge_key = f"{tid_node}_to_{cpu_node}_runtime_stat"
        add_edge_with_weight(G, tid_node, cpu_node, edge_key, "runtime_stat", runtime=runtime)

def handle_sched_process_free(row, G):
    contents = parse_contents(row['Contents'])
    comm = contents.get('comm', 'Unknown')
    tid = contents.get('tid')
    cpu_id = row['CPU']
    tid_node = f"T_{int(tid)}" if tid and tid.isdigit() else None
    cpu_node = f"CPU_{cpu_id}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"{comm} (TID {tid})")
        add_node_if_not_exists(G, cpu_node, 'CPU', f"CPU {cpu_id}")
        edge_key = f"{tid_node}_freed_on_{cpu_node}"
        add_edge_with_weight(G, tid_node, cpu_node, edge_key, "process_freed", status="terminated")

def handle_syscall_exit_epoll_wait(row, G):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    events = contents.get('events', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    file_node = f"File_{events}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_node_if_not_exists(G, file_node, 'File', f"Events FD={events}")
        edge_key = f"{tid_node}_handles_epoll_wait"
        add_edge_with_weight(G, tid_node, file_node, edge_key, "epoll_wait_exit")

def handle_syscall_exit_ioctl(row, G):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    ret = contents.get('ret', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        edge_key = f"{tid_node}_ioctl_exit"
        add_edge_with_weight(G, tid_node, tid_node, edge_key, "ioctl_exit", result=ret)

def handle_syscall_exit_splice(row, G):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    ret = contents.get('ret', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        edge_key = f"{tid_node}_splice_exit"
        add_edge_with_weight(G, tid_node, tid_node, edge_key, "splice_exit", result=ret)

def handle_syscall_exit_sync_file_range(row, G):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    ret = contents.get('ret', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        edge_key = f"{tid_node}_sync_file_range_exit"
        add_edge_with_weight(G, tid_node, tid_node, edge_key, "sync_file_range_exit", result=ret)

def handle_syscall_entry_sendmsg(row, G):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    fd = contents.get('fd', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    socket_node = f"Socket_FD_{fd}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_node_if_not_exists(G, socket_node, 'Network', f"Socket FD {fd}")
        edge_key = f"{tid_node}_uses_socket_{fd}"
        add_edge_with_weight(G, tid_node, socket_node, edge_key, "sendmsg_entry")

def handle_syscall_exit_sendmsg(row, G):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    ret = contents.get('ret', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        edge_key = f"{tid_node}_sendmsg_exit"
        add_edge_with_weight(G, tid_node, tid_node, edge_key, "sendmsg_exit", result=ret)

def handle_syscall_entry_close(row, G):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    fd = contents.get('fd', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    file_node = f"File_FD_{fd}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_node_if_not_exists(G, file_node, 'File', f"FD {fd}")
        edge_key = f"{tid_node}_close_fd_{fd}"
        add_edge_with_weight(G, tid_node, file_node, edge_key, "close_fd")

def handle_syscall_exit_close(row, G):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    ret = contents.get('ret', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        edge_key = f"{tid_node}_close_exit"
        add_edge_with_weight(G, tid_node, tid_node, edge_key, "close_exit", result=ret)

def add_entities_to_graph(row, G):
    event_type = row['Event type']
    pid = row['PID']
    tid = row['TID']
    pid_node = f"P_{int(pid)}" if pd.notna(pid) else None
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    if pid_node:
        add_node_if_not_exists(G, pid_node, 'Process', f"Process {pid}")
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
    if pid_node and tid_node and not G.has_edge(pid_node, tid_node):
        G.add_edge(pid_node, tid_node, relationship='contains')
    handlers = {
        'sched_waking': handle_sched_waking,
        'sched_wakeup': handle_sched_wakeup,
        'sched_switch': handle_sched_switch,
        'syscall_entry_ioctl': handle_syscall_entry_ioctl,
        'syscall_entry_splice': handle_syscall_entry_splice,
        'syscall_entry_sync_file_range': handle_syscall_entry_sync_file_range,
        'sched_stat_runtime': handle_sched_stat_runtime,
        'syscall_exit_epoll_wait': handle_syscall_exit_epoll_wait,
        'syscall_exit_ioctl': handle_syscall_exit_ioctl,
        'syscall_exit_splice': handle_syscall_exit_splice,
        'syscall_exit_sync_file_range': handle_syscall_exit_sync_file_range,
        'sched_process_free': handle_sched_process_free,
        'syscall_entry_sendmsg': handle_syscall_entry_sendmsg,
        'syscall_exit_sendmsg': handle_syscall_exit_sendmsg,
        'syscall_entry_close': handle_syscall_entry_close,
        'syscall_exit_close': handle_syscall_exit_close,
    }
    handler = handlers.get(event_type)
    if handler:
        handler(row, G)

def main():
    data = pd.read_csv('../trace_data/run0_0.csv')
    G = nx.MultiDiGraph()
    for _, row in data.iterrows():
        add_entities_to_graph(row, G)
    color_map = {
        'Process': 'lightblue',
        'Thread': 'green',
        'CPU': 'red',
        'Memory': 'yellow',
        'File': 'orange',
        'Network': 'pink',
        'Disk': 'purple',
        'IPC': 'brown',
        'Timer': 'gold',
        'default': 'grey'
    }
    node_colors = [color_map.get(G.nodes[node]['entity'], color_map['default']) for node in G]
    pos = nx.spring_layout(G, k=0.5)
    plt.figure(figsize=(15, 15))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1900, alpha=0.6)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(keys=True), width=2,
                           arrowstyle='->', arrowsize=20, connectionstyle='arc3,rad=0.1')
    relationship_summary = {}
    edge_labels = {}
    for u, v, key, data in G.edges(data=True, keys=True):
        relationship = data['relationship']
        if (u, v) not in relationship_summary:
            relationship_summary[(u, v)] = {}
        if relationship not in relationship_summary[(u, v)]:
            relationship_summary[(u, v)][relationship] = 0
        relationship_summary[(u, v)][relationship] += 1
        edge_labels[(u, v)] = sum(relationship_summary[(u, v)].values())
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8, font_weight='bold')
    nx.draw_networkx_labels(G, pos, font_size=10)
    plt.title("Kernel Events Knowledge Graph")
    plt.legend(handles=[mpatches.Patch(color=color, label=entity) for entity, color in color_map.items()],
               title="Entity Types", loc='upper left')
    plt.axis('off')
    plt.show()
    relationship_summary_str_keys = {f"{u}_{v}": relationships for (u, v), relationships in relationship_summary.items()}
    with open('../knowledge_graph_output/relationship_details.json', 'w') as f:
        json.dump(relationship_summary_str_keys, f, indent=4)
    data_json = json_graph.node_link_data(G)
    with open('../knowledge_graph_output/knowledge_graph.json', 'w') as f:
        json.dump(data_json, f, indent=4)

if __name__ == "__main__":
    main()
