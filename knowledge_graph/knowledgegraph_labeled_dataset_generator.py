import pandas as pd
import networkx as nx
import json
from networkx.readwrite import json_graph
import csv


# Utility functions
def parse_contents(contents_str):
    contents_dict = {}
    for pair in contents_str.split(','):
        key_value = pair.strip().split('=')
        if len(key_value) == 2:
            key, value = key_value
            contents_dict[key.strip()] = value.strip()
    return contents_dict


def add_node_if_not_exists(G, node_id, entity_type, label, **attributes):
    if node_id and not G.has_node(node_id):
        G.add_node(node_id, entity=entity_type, label=label, **attributes)


def add_edge_with_weight(G, u, v, relationship, triplets, **kwargs):
    if u and v:
        key = f"{u}_{relationship}_{v}"
        if G.has_edge(u, v, key=key):
            G[u][v][key]['weight'] += 1
        else:
            G.add_edge(u, v, key=key, relationship=relationship, weight=1, **kwargs)
            # Add the triplet to the list
            triplet = {
                'source': u,
                'target': v,
                'relationship': relationship,
                'weight': 1  # Initialize weight
            }
            # Include additional properties if any
            triplet.update(kwargs)
            triplets.append(triplet)
        # Update the weight in the triplet
        for triplet in triplets:
            if triplet['source'] == u and triplet['target'] == v and triplet['relationship'] == relationship:
                triplet['weight'] = G[u][v][key]['weight']
                break


# Handler functions
def handle_sched_waking(row, G, triplets):
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
            add_edge_with_weight(G, tid_node, cpu_node, 'scheduled_to_wake_on', triplets)


def handle_sched_wakeup(row, G, triplets):
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
            add_edge_with_weight(G, tid_node, cpu_node, 'wake_up', triplets)


def handle_sched_switch(row, G, triplets):
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
        add_edge_with_weight(G, prev_tid_node, cpu_node, 'switched_out', triplets)
    if next_tid_node:
        add_node_if_not_exists(G, next_tid_node, 'Thread', f"{next_comm} ({next_tid_node})")
        add_edge_with_weight(G, cpu_node, next_tid_node, 'switched_in', triplets)


def handle_syscall_entry_ioctl(row, G, triplets):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    fd = contents.get('fd', 'Unknown')
    cmd = contents.get('cmd', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    file_node = f"File_{fd}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_node_if_not_exists(G, file_node, 'File', f"FD={fd}")
        add_edge_with_weight(G, tid_node, file_node, 'ioctl', triplets, cmd=cmd)


def handle_syscall_entry_splice(row, G, triplets):
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
        add_edge_with_weight(G, tid_node, file_node_in, 'splice_in', triplets)
        add_edge_with_weight(G, tid_node, file_node_out, 'splice_out', triplets)


def handle_syscall_entry_sync_file_range(row, G, triplets):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    fd = contents.get('fd', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    file_node = f"File_{fd}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_node_if_not_exists(G, file_node, 'File', f"FD={fd}")
        add_edge_with_weight(G, tid_node, file_node, 'sync_file', triplets)


def handle_sched_stat_runtime(row, G, triplets):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    cpu_id = row['CPU']
    runtime = contents.get('runtime', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    cpu_node = f"CPU_{cpu_id}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_node_if_not_exists(G, cpu_node, 'CPU', f"CPU {cpu_id}")
        add_edge_with_weight(G, tid_node, cpu_node, 'runtime_stat', triplets, runtime=runtime)


def handle_sched_process_free(row, G, triplets):
    contents = parse_contents(row['Contents'])
    comm = contents.get('comm', 'Unknown')
    tid = contents.get('tid')
    cpu_id = row['CPU']
    tid_node = f"T_{int(tid)}" if tid and tid.isdigit() else None
    cpu_node = f"CPU_{cpu_id}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"{comm} (TID {tid})")
        add_node_if_not_exists(G, cpu_node, 'CPU', f"CPU {cpu_id}")
        add_edge_with_weight(G, tid_node, cpu_node, 'process_freed', triplets, status="terminated")


def handle_syscall_exit_epoll_wait(row, G, triplets):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    events = contents.get('events', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    file_node = f"File_{events}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_node_if_not_exists(G, file_node, 'File', f"Events FD={events}")
        add_edge_with_weight(G, tid_node, file_node, 'epoll_wait_exit', triplets)


def handle_syscall_exit_ioctl(row, G, triplets):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    ret = contents.get('ret', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_edge_with_weight(G, tid_node, tid_node, 'ioctl_exit', triplets, result=ret)


def handle_syscall_exit_splice(row, G, triplets):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    ret = contents.get('ret', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_edge_with_weight(G, tid_node, tid_node, 'splice_exit', triplets, result=ret)


def handle_syscall_exit_sync_file_range(row, G, triplets):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    ret = contents.get('ret', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_edge_with_weight(G, tid_node, tid_node, 'sync_file_range_exit', triplets, result=ret)


def handle_syscall_entry_sendmsg(row, G, triplets):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    fd = contents.get('fd', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    socket_node = f"Socket_FD_{fd}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_node_if_not_exists(G, socket_node, 'Network', f"Socket FD {fd}")
        add_edge_with_weight(G, tid_node, socket_node, 'sendmsg_entry', triplets)


def handle_syscall_exit_sendmsg(row, G, triplets):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    ret = contents.get('ret', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_edge_with_weight(G, tid_node, tid_node, 'sendmsg_exit', triplets, result=ret)


def handle_syscall_entry_close(row, G, triplets):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    fd = contents.get('fd', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    file_node = f"File_FD_{fd}"
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_node_if_not_exists(G, file_node, 'File', f"FD {fd}")
        add_edge_with_weight(G, tid_node, file_node, 'close_fd', triplets)


def handle_syscall_exit_close(row, G, triplets):
    contents = parse_contents(row['Contents'])
    tid = row['TID']
    ret = contents.get('ret', 'Unknown')
    tid_node = f"T_{int(tid)}" if pd.notna(tid) else None
    if tid_node:
        add_node_if_not_exists(G, tid_node, 'Thread', f"Thread {tid}")
        add_edge_with_weight(G, tid_node, tid_node, 'close_exit', triplets, result=ret)


def add_entities_to_graph(row, G, triplets):
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
        # Add to triplets
        triplet = {
            'source': pid_node,
            'target': tid_node,
            'relationship': 'contains',
            'weight': 1
        }
        triplets.append(triplet)
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
        handler(row, G, triplets)


def main():
    # Load your trace data CSV file
    data = pd.read_csv('../trace_data/run0_0.csv')

    G = nx.MultiDiGraph()
    triplets = []  # List to store triplets for ML

    # Iterate over the rows and construct the graph
    for _, row in data.iterrows():
        add_entities_to_graph(row, G, triplets)

    # Save the triplets to a CSV file for ML
    with open('../output/knowledge_graph_output/kg_triplets.csv', 'w', newline='') as csvfile:
        fieldnames = ['source', 'relationship', 'target', 'weight']
        # Include any additional properties from the triplets
        additional_fields = set()
        for triplet in triplets:
            additional_fields.update(triplet.keys())
        additional_fields -= set(fieldnames)
        fieldnames.extend(additional_fields)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for triplet in triplets:
            writer.writerow(triplet)

    # Optionally, you can save the graph in JSON format
    data_json = json_graph.node_link_data(G)
    with open('../output/knowledge_graph_output/knowledge_graph.json', 'w') as f:
        json.dump(data_json, f, indent=4)


if __name__ == "__main__":
    main()
