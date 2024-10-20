import pandas as pd

class EventTranslator:
    def __init__(self, dataframe):
        self.df = dataframe
    def describe_power_cpu_idle(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        state = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        context_cpu_id = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        return (
            f"At {timestamp}, CPU {cpu_id} entered idle state with state code {state} "
            f"on context CPU {context_cpu_id}."
        )
    def describe_sched_switch(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        prev_comm = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        prev_tid = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        prev_prio = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'
        prev_state = contents[3].split('=')[1] if len(contents) > 3 else 'unknown'
        next_comm = contents[4].split('=')[1] if len(contents) > 4 else 'unknown'
        next_tid = contents[5].split('=')[1] if len(contents) > 5 else 'unknown'
        next_prio = contents[6].split('=')[1] if len(contents) > 6 else 'unknown'

        description = (
            f"At {timestamp}, CPU {cpu_id} switched from task {prev_comm} (TID {prev_tid}, "
            f"priority {prev_prio}, state {prev_state}) to task {next_comm} (TID {next_tid}, priority {next_prio})."
        )
        return description
    def describe_kmem_kmalloc(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        call_site = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        ptr = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        bytes_req = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'
        bytes_alloc = contents[3].split('=')[1] if len(contents) > 3 else 'unknown'
        gfp_flags = contents[4].split('=')[1] if len(contents) > 4 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, a memory allocation was made at call site {call_site}. "
            f"Pointer {ptr} was allocated with {bytes_req} bytes requested and {bytes_alloc} bytes allocated. "
            f"GFP flags: {gfp_flags}."
        )
        return description
    def describe_kmem_kfree(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        call_site = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        ptr = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, a memory deallocation was made at call site {call_site}. "
            f"Pointer {ptr} was freed."
        )
        return description
    def describe_sched_waking(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        comm = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        tid = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        prio = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'
        target_cpu = contents[3].split('=')[1] if len(contents) > 3 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, task {comm} (TID {tid}, priority {prio}) was waking up "
            f"and targeting CPU {target_cpu}."
        )
        return description
    def describe_sched_wakeup(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        comm = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        tid = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        prio = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'
        target_cpu = contents[3].split('=')[1] if len(contents) > 3 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, task {comm} (TID {tid}, priority {prio}) woke up "
            f"and targeted CPU {target_cpu}."
        )
        return description
    def describe_rcu_utilization(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        s = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, RCU utilization event occurred with status: {s}."
        )
        return description
    def describe_syscall_exit_epoll_wait(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        ret = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        events = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, the epoll_wait system call exited with return value {ret}. "
            f"Events: {events}."
        )
        return description
    def describe_kmem_cache_alloc(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        call_site = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        ptr = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        bytes_req = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'
        bytes_alloc = contents[3].split('=')[1] if len(contents) > 3 else 'unknown'
        gfp_flags = contents[4].split('=')[1] if len(contents) > 4 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, a cache memory allocation was made at call site {call_site}. "
            f"Pointer {ptr} was allocated with {bytes_req} bytes requested and {bytes_alloc} bytes allocated. "
            f"GFP flags: {gfp_flags}."
        )
        return description
    def describe_syscall_entry_ioctl(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        fd = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        cmd = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        arg = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, the ioctl system call was entered with file descriptor {fd}, "
            f"command {cmd}, and argument {arg}."
        )
        return description
    def describe_x86_irq_vectors_call_function_entry(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        vector = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, an interrupt vector {vector} entry occurred. "
        )
        return description
    def describe_x86_irq_vectors_call_function_exit(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        vector = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, an interrupt vector {vector} exit occurred. "
        )
        return description
    def describe_kmem_cache_free(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        call_site = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        ptr = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, a memory cache was freed at call site {call_site}. "
            f"Pointer {ptr} was freed from the cache."
        )
        return description
    def describe_syscall_exit_ioctl(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        ret = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        arg = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, an ioctl syscall exited with return value {ret}. "
            f"Argument: {arg}."
        )
        return description
    def describe_syscall_entry_splice(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        fd_in = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        off_in = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        fd_out = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'
        off_out = contents[3].split('=')[1] if len(contents) > 3 else 'unknown'
        len_splice = contents[4].split('=')[1] if len(contents) > 4 else 'unknown'
        flags = contents[5].split('=')[1] if len(contents) > 5 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, a splice system call was initiated. Data is being transferred "
            f"from file descriptor {fd_in} at offset {off_in} to file descriptor {fd_out} at offset {off_out}. "
            f"Length of data to transfer: {len_splice} bytes. Flags used: {flags}."
        )
        return description
    def describe_kmem_mm_page_alloc(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        page = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        pfn = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        order = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'
        gfp_flags = contents[3].split('=')[1] if len(contents) > 3 else 'unknown'
        migratetype = contents[4].split('=')[1] if len(contents) > 4 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, a memory page allocation occurred. Page at address {page} "
            f"with page frame number (PFN) {pfn} of order {order} was allocated. GFP flags used: {gfp_flags}. "
            f"Migrate type: {migratetype}."
        )
        return description
    def describe_syscall_exit_splice(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        ret = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, the splice system call exited with return value {ret}."
        )
        return description
    def describe_writeback_mark_inode_dirty(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        name = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        ino = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        state = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'
        flags = contents[3].split('=')[1] if len(contents) > 3 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, the inode {name} with inode number {ino} was marked dirty. "
            f"State: {state}, Flags: {flags}."
        )
        return description
    def describe_writeback_dirty_inode_start(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        name = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        ino = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        state = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'
        flags = contents[3].split('=')[1] if len(contents) > 3 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, the start of writeback for inode {name} with inode number {ino} was initiated. "
            f"State: {state}, Flags: {flags}."
        )
        return description
    def describe_block_touch_buffer(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        dev = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        sector = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        size = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, the block device with dev ID {dev} had a buffer touch at sector {sector}. "
            f"Buffer size: {size} bytes."
        )
        return description
    def describe_writeback_dirty_inode(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        name = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        ino = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        state = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'
        flags = contents[3].split('=')[1] if len(contents) > 3 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, inode {ino} on device {name} was marked dirty with flags {flags}. "
            f"State after operation: {state}."
        )
        return description
    def describe_block_dirty_buffer(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        dev = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        sector = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        size = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, a buffer for device {dev} "
            f"at sector {sector} of size {size} bytes was marked dirty."
        )
        return description
    def describe_writeback_dirty_page(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        name = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        ino = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        index = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, page index {index} of inode {ino} on device {name} "
            f"was marked as dirty for writeback."
        )
        return description
    def describe_kmem_mm_page_free(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        contents = row['Contents'].split(', ')
        page = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        pfn = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        order = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'

        description = (
            f"At {timestamp}, on CPU {cpu_id}, the memory page at {page} with page frame number {pfn} "
            f"and order {order} was freed."
        )
        return description
    def describe_syscall_entry_sync_file_range(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        contents = row['Contents'].split(', ')
        fd = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        offset = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        nbytes = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'
        flags = contents[3].split('=')[1] if len(contents) > 3 else 'unknown'

        description = (
            f"At {timestamp}, CPU {cpu_id}, TID {tid}, Priority {prio}: "
            f"a sync_file_range syscall was initiated with file descriptor {fd}, "
            f"offset {offset}, nbytes {nbytes}, and flags {flags}."
        )
        return description
    def describe_block_bio_remap(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        contents = row['Contents'].split(', ')
        dev = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        sector = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        nr_sector = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'
        rwbs = contents[3].split('=')[1] if len(contents) > 3 else 'unknown'
        old_dev = contents[4].split('=')[1] if len(contents) > 4 else 'unknown'
        old_sector = contents[5].split('=')[1] if len(contents) > 5 else 'unknown'

        rwbs_description = "read and write" if "rw" in rwbs else "read-only" if "r" in rwbs else "write-only"

        description = (
            f"At {timestamp}, a remapping operation was recorded on CPU {cpu_id} by TID {tid} with priority {prio}. "
            f"The operation involved remapping {nr_sector} sectors starting at sector {sector} on device {dev}. "
            f"This operation, characterized by its {rwbs_description} status, redirected I/O from sector {old_sector} "
            f"on device {old_dev} to the new location. This is crucial for optimizing I/O operations and managing device wear."
        )
        return description
    def describe_kmem_kmalloc_node(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        contents = row['Contents'].split(', ')
        call_site = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'
        ptr = contents[1].split('=')[1] if len(contents) > 1 else 'unknown'
        bytes_req = contents[2].split('=')[1] if len(contents) > 2 else 'unknown'
        bytes_alloc = contents[3].split('=')[1] if len(contents) > 3 else 'unknown'
        gfp_flags = contents[4].split('=')[1] if len(contents) > 4 else 'unknown'
        node = contents[5].split('=')[1] if len(contents) > 5 else 'unknown'

        node_info = f"on NUMA node {node}" if node != "-1" else "without a specific NUMA node preference"

        description = (
            f"On {timestamp}, a memory allocation request was processed on CPU {cpu_id}, managed by thread ID {tid} with priority {prio}. "
            f"The system executed a memory allocation at the call site {call_site}, "
            f"resulting in the allocation of a memory block at pointer {ptr} with {bytes_alloc} bytes out of the {bytes_req} bytes requested. "
            f"This operation was performed with GFP flags {gfp_flags}, {node_info}. "
            f"This memory allocation is critical for the process's resource management and efficiency."
        )
        return description
    def describe_syscall_exit_sync_file_range(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        contents = row['Contents'].split(', ')
        ret = contents[0].split('=')[1] if len(contents) > 0 else 'unknown'

        success_state = "successfully" if ret == "0" else "with an error code of " + ret

        description = (
            f"At {timestamp}, a 'sync_file_range' system call completed on CPU {cpu_id} "
            f"managed by thread ID {tid} with priority {prio}. The operation concluded {success_state}, "
            f"indicating the final status of the file synchronization attempt. "
            f"This system call is essential for controlling when file data is committed to storage, enhancing data integrity and performance."
        )
        return description
    def describe_sched_stat_runtime(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        comm = row['Contents'].split(', ')[0].split('=')[1]
        runtime = row['Contents'].split(', ')[1].split('=')[1]
        vruntime = row['Contents'].split(', ')[2].split('=')[1]

        description = (
            f"At {timestamp}, the process '{comm}' (TID {tid}, Priority {prio}) on CPU {cpu_id} recorded a scheduler runtime. "
            f"The actual runtime was {runtime} nanoseconds, while the virtual runtime, which accounts for task fairness, was {vruntime} nanoseconds. "
            f"This data helps in understanding the scheduling behavior and performance isolation between different tasks."
        )
        return description
    def describe_power_cpu_frequency(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        state = row['Contents'].split(', ')[0].split('=')[1]
        tid = row['TID']
        prio = row['Prio']

        description = (
            f"At {timestamp}, CPU {cpu_id} adjusted its operating frequency to {state} Hz. "
            f"This frequency adjustment reflects changes aimed at optimizing performance or energy usage. "
            f"Task ID (TID) {tid} with priority {prio} was actively scheduled during this change."
        )
        return description
    def describe_sched_process_free(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        comm = row['Contents'].split(', ')[0].split('=')[1]
        tid = row['TID']
        prio = row['Prio']

        description = (
            f"At {timestamp}, on CPU {cpu_id}, the process '{comm}' with Task ID (TID) {tid} and priority {prio} "
            f"was released from scheduling. This typically occurs when a process is terminated or completes its execution, "
            f"freeing up system resources."
        )
        return description
    def describe_syscall_entry_sendmsg(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        fd = row['Contents'].split(', ')[0].split('=')[1]
        msg_address = row['Contents'].split(', ')[1].split('=')[1]
        flags = row['Contents'].split(', ')[2].split('=')[1]
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']

        flags_description = "none" if flags == "0" else f"flags value {flags}"
        description = (
            f"At {timestamp}, process ID {pid}, TID {tid}, priority {prio} on CPU {cpu_id}: "
            f"Initiated 'sendmsg' system call on file descriptor {fd}. Message is located at memory address {msg_address}, "
            f"with {flags_description}. This system call is typically used for sending messages through a socket."
        )
        return description
    def describe_syscall_exit_sendmsg(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        ret_value = row['Contents'].split('=')[1]
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']

        success_status = "successfully" if ret_value == "0" else f"with return code {ret_value}"
        description = (
            f"At {timestamp}, process ID {pid}, TID {tid}, priority {prio} on CPU {cpu_id}: "
            f"Completed 'sendmsg' system call {success_status}. This call is typically used to send a message "
            f"through a socket and any return value other than zero indicates an error or the number of bytes sent."
        )
        return description
    def describe_syscall_entry_close(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        fd = row['Contents'].split('=')[1]
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']

        description = (
            f"At {timestamp}, process with ID {pid} (TID {tid}, priority {prio}), running on CPU {cpu_id}, "
            f"began the process of closing file descriptor {fd}. This action frees up the file descriptor to be reused, "
            f"ensuring that system resources are efficiently managed."
        )
        return description
    def describe_syscall_exit_close(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        ret = row['Contents'].split(',')[0].split('=')[1]
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']

        success_statement = "successfully" if int(ret) == 0 else "unsuccessfully"

        description = (
            f"On {timestamp}, the system call to close a file descriptor by process {pid} "
            f"(Thread ID: {tid}, Priority: {prio}), running on CPU {cpu_id}, completed {success_statement}. "
            f"The attempt to release the file descriptor returned a status of {ret}, indicating "
            f"{'no errors' if int(ret) == 0 else 'an error with code ' + ret}."
        )
        return description
    def describe_syscall_entry_epoll_wait(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        epfd = row['Contents'].split(', ')[0].split('=')[1]
        maxevents = row['Contents'].split(', ')[1].split('=')[1]
        timeout = row['Contents'].split(', ')[2].split('=')[1]
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']

        description = (
            f"At {timestamp}, process {pid} with TID {tid} and priority {prio}, running on CPU {cpu_id}, "
            f"initiated an epoll_wait system call using file descriptor {epfd}. It is configured to monitor "
            f"up to {maxevents} events with a timeout of {'indefinitely' if int(timeout) == -1 else timeout + ' milliseconds'}."
        )
        return description
    def describe_sched_migrate_task(self, row):
        timestamp = row['Timestamp']
        orig_cpu = row['Contents'].split(', ')[3].split('=')[1]
        dest_cpu = row['Contents'].split(', ')[4].split('=')[1]
        comm = row['Contents'].split(', ')[0].split('=')[1]
        tid = row['TID']
        prio = row['Prio']

        description = (
            f"At {timestamp}, a task migration event occurred on CPU {orig_cpu}. The task from process '{comm}', "
            f"with TID {tid} and priority {prio}, was transferred from CPU {orig_cpu} to CPU {dest_cpu}. "
            f"This adjustment is typically performed to optimize process execution and load balancing across CPUs."
        )
        return description
    def describe_syscall_exit_recvmsg(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(', ')[0].split('=')[1]
        msg = row['Contents'].split(', ')[1].split('=')[1]

        # Assessing the outcome of the syscall
        status = "successfully" if int(ret) == 0 else "unsuccessfully"

        description = (
            f"At {timestamp}, the 'recvmsg' syscall executed on CPU {cpu_id} by process {pid} (TID {tid}, priority {prio}) "
            f"completed {status}. The operation targeted the message buffer at address {msg}, returning a status code of {ret}."
        )
        return description
    def describe_syscall_entry_shutdown(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        fd = row['Contents'].split(', ')[0].split('=')[1]
        how = row['Contents'].split(', ')[1].split('=')[1]

        # Decoding the 'how' parameter for better readability
        shutdown_method = {
            '0': 'SHUT_RD (disables further receive operations)',
            '1': 'SHUT_WR (disables further send operations)',
            '2': 'SHUT_RDWR (disables further send and receive operations)'
        }.get(how, 'an unknown method')

        description = (
            f"At {timestamp}, on CPU {cpu_id}, process {pid} (TID {tid}, priority {prio}) initiated a 'shutdown' syscall for file descriptor {fd}. "
            f"The operation was carried out with {shutdown_method}. This action is generally performed to close either one or both communication directions of the socket."
        )
        return description
    def describe_syscall_exit_shutdown(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(', ')[0].split('=')[1]

        # Assessing the outcome of the syscall
        status = "successfully" if int(ret) == 0 else "unsuccessfully"

        description = (
            f"At {timestamp}, the 'shutdown' syscall executed on CPU {cpu_id} by process {pid} (TID {tid}, priority {prio}) "
            f"completed {status}. The result was {ret}, indicating that the operation {status} terminated the socket connection or part of it."
        )
        return description
    def describe_syscall_entry_newfstat(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        fd = row['Contents'].split(', ')[0].split('=')[1]

        description = (
            f"At {timestamp}, on CPU {cpu_id}, the process with PID {pid} and TID {tid} initiated a 'newfstat' syscall "
            f"to retrieve status information for the file descriptor {fd}. This operation is commonly used to obtain file "
            f"attributes such as size, permissions, and modification time."
        )
        return description
    def describe_syscall_exit_newfstat(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(', ')[0].split('=')[1]
        statbuf = row['Contents'].split(', ')[1].split('=')[1]

        # Assessing the outcome of the syscall
        status = "successfully" if int(ret) == 0 else "unsuccessfully"

        description = (
            f"At {timestamp}, on CPU {cpu_id}, the 'newfstat' syscall executed by process {pid} (TID {tid}, priority {prio}) "
            f"completed {status}. It attempted to obtain file statistics, storing the data at memory address {statbuf}. "
            f"The operation returned a status code of {ret}, indicating that the file attributes were {status} retrieved."
        )
        return description
    def describe_syscall_entry_mmap(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        contents = row['Contents'].split(', ')
        addr = contents[0].split('=')[1]
        length = contents[1].split('=')[1]
        prot = contents[2].split('=')[1]
        flags = contents[3].split('=')[1]
        fd = contents[4].split('=')[1]
        offset = contents[5].split('=')[1]

        # Mapping description based on protection
        protection_desc = "read/write" if int(prot) == 3 else "read-only"

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a memory mapping request. "
            f"The request was to map {length} bytes starting from address {addr}, with {protection_desc} access. "
            f"The mapping is associated with file descriptor {fd} at offset {offset}. The flags used in this operation were {flags}."
        )
        return description
    def describe_syscall_exit_mmap(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(',')[0].split('=')[1]

        description = (
            f"At {timestamp}, the 'mmap' syscall completed for process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id}. "
            f"The system call returned a memory address at {ret}, indicating a successful memory mapping."
        )
        return description
    def describe_syscall_entry_write(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        fd = row['Contents'].split(', ')[0].split('=')[1]
        buf = row['Contents'].split(', ')[1].split('=')[1]
        count = row['Contents'].split(', ')[2].split('=')[1]

        description = (
            f"At {timestamp}, on CPU {cpu_id}, the process {pid} with TID {tid} and priority {prio} initiated a 'write' syscall "
            f"using file descriptor {fd}. The syscall attempts to write {count} bytes from the buffer at address {buf}. "
            f"This operation is crucial for handling data output to files, sockets, or other communication interfaces."
        )
        return description
    def describe_syscall_exit_write(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(', ')[0].split('=')[1]

        # Assessing the outcome of the write operation
        status = "successfully" if int(ret) > 0 else "unsuccessfully"

        description = (
            f"At {timestamp}, the 'write' syscall on CPU {cpu_id} for process {pid} with TID {tid} and priority {prio} completed {status}. "
            f"The operation attempted to write data, resulting in {ret} bytes being written. "
            f"This outcome indicates how much data was actually transferred during the syscall."
        )
        return description
    def describe_syscall_entry_exit_group(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        error_code = row['Contents'].split(', ')[0].split('=')[1]

        # Determining the outcome based on the error code
        if int(error_code) == 0:
            outcome = "successfully, indicating a clean and orderly shutdown of all threads within the process group."
        else:
            outcome = f"with an error code of {error_code}, suggesting issues during the termination process that may require further investigation."

        description = (
            f"At {timestamp} on CPU {cpu_id}, the process (PID {pid}) initiated a shutdown sequence for all associated threads via the 'exit_group' syscall. "
            f"This termination, executed by thread ID {tid} with priority level {prio}, concluded {outcome} This system call is critical for releasing resources "
            "and ensuring that all threads end their execution without leaving unfinished tasks or memory leaks."
        )
        return description
    def describe_sched_process_exit(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        comm = row['Contents'].split(', ')[0].split('=')[1]

        description = (
            f"At {timestamp}, on CPU {cpu_id}, the process '{comm}' with PID {pid} completed its execution. "
            f"The thread ID {tid}, operating at a priority level of {prio}, has successfully exited. This event marks the end of the process's lifecycle on the system, "
            "releasing all allocated resources and making way for new processes to utilize the computing capacity."
        )
        return description
    def describe_syscall_exit_wait4(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(', ')[0].split('=')[1]
        stat_addr = row['Contents'].split(', ')[1].split('=')[1]
        ru = row['Contents'].split(', ')[2].split('=')[1]

        # Assessing the outcome of the syscall
        status = "successfully" if int(ret) >= 0 else "with an error"

        description = (
            f"At {timestamp}, on CPU {cpu_id}, the 'wait4' system call completed for process {pid} (TID {tid}, priority {prio}). "
            f"The call terminated {status}, returning the PID {ret} of the exited child process. "
            f"Status information was stored at address {stat_addr}, and resource usage data at {ru}."
        )
        return description
    def describe_syscall_entry_rt_sigaction(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        sig = row['Contents'].split(', ')[0].split('=')[1]
        act = row['Contents'].split(', ')[1].split('=')[1]
        sigsetsize = row['Contents'].split(', ')[2].split('=')[1]

        description = (
            f"At {timestamp}, the process with ID {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} issued a 'rt_sigaction' system call "
            f"to modify how signal {sig} is handled. The address for the new action settings is at {act}, "
            f"with a signal set size of {sigsetsize} bytes, indicating the context within which the new settings will be applied."
        )
        return description
    def describe_syscall_exit_rt_sigaction(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(', ')[0].split('=')[1]
        oact = row['Contents'].split(', ')[1].split('=')[1]

        # Checking the return value to determine the status of the syscall
        status = "successfully" if int(ret) == 0 else "unsuccessfully"

        description = (
            f"At {timestamp}, the 'rt_sigaction' syscall completed {status} on CPU {cpu_id} for process {pid} (TID {tid}, priority {prio}). "
            f"The operation was intended to update signal handling settings; the old action settings were saved at memory address {oact}. "
            f"The return status of this system call is {ret}, indicating whether the request was handled properly."
        )
        return description
    def describe_syscall_entry_rt_sigprocmask(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        how = row['Contents'].split(', ')[0].split('=')[1]
        nset = row['Contents'].split(', ')[1].split('=')[1]
        sigsetsize = row['Contents'].split(', ')[2].split('=')[1]

        # Translating the 'how' parameter to more understandable terms
        how_description = {
            '1': 'block',
            '2': 'unblock',
            '3': 'set'
        }.get(how, 'unknown operation')

        description = (
            f"At {timestamp}, the process {pid} (TID {tid}, priority {prio}) initiated a syscall on CPU {cpu_id} to {how_description} signals. "
            f"The new set of signals to be modified is at memory address {nset} with a size of {sigsetsize} bytes. "
            f"This operation modifies which signals the thread is blocking."
        )
        return description
    def describe_syscall_exit_rt_sigprocmask(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(', ')[0].split('=')[1]
        oset = row['Contents'].split(', ')[1].split('=')[1]

        status = "successfully" if int(ret) == 0 else "unsuccessfully"

        description = (
            f"At {timestamp}, the 'rt_sigprocmask' syscall completed {status} on CPU {cpu_id} for process {pid} (TID {tid}, priority {prio}). "
            f"The attempt to modify the signal mask returned {ret}, with the old set located at memory address {oset}. "
            f"This system call adjusts the set of blocked signals, which is crucial for managing signal handling behavior in a process."
        )
        return description
    def describe_syscall_entry_wait4(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        upid = row['Contents'].split(', ')[0].split('=')[1]
        options = row['Contents'].split(', ')[1].split('=')[1]

        description = (
            f"At {timestamp}, the process with PID {pid} (thread ID {tid}, running on CPU {cpu_id}, priority {prio}) "
            f"issued a system call to wait for changes in the process with ID {upid}. The system call was initiated with options set to {options}, "
            f"which regulate how the wait is performed. This syscall is typically used to pause the calling process until one of its child processes changes state, "
            f"indicating an exit or interruption."
        )
        return description
    def describe_sched_process_wait(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        comm = row['Contents'].split(', ')[0].split('=')[1]

        description = (
            f"At {timestamp}, the process '{comm}' with PID {pid} (TID {tid}, running on CPU {cpu_id}, priority {prio}) "
            f"entered a wait state. This is typically indicative of the process waiting for either a particular condition "
            f"to be met or for an event to occur, suggesting a synchronization or dependency on other processes or system "
            f"resources. The specific reasons and mechanics behind the wait can vary, often depending on system state and "
            f"inter-process communication mechanisms."
        )
        return description
    def describe_syscall_entry_unknown(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        syscall_id = row['Contents'].split(', ')[0].split('=')[1]
        args = [row['Contents'].split(', ')[i].split('=')[1] for i in range(1, 6)]

        description = (
            f"At {timestamp}, an unknown syscall with ID {syscall_id} was initiated on CPU {cpu_id} by process {pid} "
            f"(TID {tid}, priority {prio}). The syscall was called with the following arguments: {args}. Due to the "
            f"unknown nature of the syscall, the specifics of its functionality and potential impact on the system "
            f"are not immediately discernible from the trace data alone. This may require further investigation "
            f"or consultation with more detailed system documentation or source code."
        )
        return description
    def describe_syscall_entry_read(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        fd = row['Contents'].split(', ')[0].split('=')[1]
        count = row['Contents'].split(', ')[1].split('=')[1]

        description = (
            f"On {timestamp}, the process identified by PID {pid} (thread ID {tid}, priority level {prio}) "
            f"initiated a 'read' system call on CPU {cpu_id}. This operation targets file descriptor {fd}, "
            f"attempting to retrieve {count} bytes. The file descriptor refers to a resource like a file, "
            f"device, or socket. The outcome, including the number of bytes successfully read, will depend on "
            f"the characteristics of the resource, such as availability and data readiness."
        )
        return description
    def describe_syscall_exit_read(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(', ')[0].split('=')[1]
        buf = row['Contents'].split(', ')[1].split('=')[1]

        successful_read = "successfully" if int(ret) > 0 else "unsuccessfully"
        data_read = f"{ret} bytes" if int(ret) > 0 else "no data"

        description = (
            f"At {timestamp}, the read operation requested by process {pid} (TID {tid}, priority {prio}) "
            f"on CPU {cpu_id} completed {successful_read}. It attempted to read data into buffer at address {buf}, "
            f"and managed to read {data_read}. This result is indicative of the availability and readiness of the "
            f"data in the file or device associated with the operation."
        )
        return description
    def describe_syscall_entry_lseek(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        fd = row['Contents'].split(', ')[0].split('=')[1]
        offset = row['Contents'].split(', ')[1].split('=')[1]
        whence = row['Contents'].split(', ')[2].split('=')[1]

        # Interpreting 'whence' parameter for clarity
        whence_description = {
            '0': 'from the beginning of the file',
            '1': 'from the current file position',
            '2': 'from the end of the file'
        }.get(whence, 'an unknown reference point')

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'lseek' system call "
            f"to change the file position. The operation targeted file descriptor {fd}, attempting to adjust the position "
            f"to {offset} bytes {whence_description}. This call is often used to reposition the read/write file offset, "
            f"facilitating operations such as file searching or data appending."
        )
        return description
    def describe_syscall_exit_lseek(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(', ')[0].split('=')[1]

        # Check for a successful lseek return
        status = "successfully" if int(ret) >= 0 else "unsuccessfully"
        new_position = f"to position {ret}" if int(ret) >= 0 else "due to an error"

        description = (
            f"At {timestamp}, the 'lseek' system call by process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed {status}. "
            f"The call attempted to adjust the file's read/write position {new_position}. This result indicates whether the attempt "
            f"to move within the file was feasible or encountered obstacles, such as attempting to seek beyond the file's current end."
        )
        return description
    def describe_syscall_entry_clone(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        clone_flags = row['Contents'].split(', ')[0].split('=')[1]
        newsp = row['Contents'].split(', ')[1].split('=')[1]
        parent_tid = row['Contents'].split(', ')[2].split('=')[1]
        child_tid = row['Contents'].split(', ')[3].split('=')[1]

        flag_description = "with child thread running in a new stack space" if newsp != '0x0' else "within the same stack space as the parent"
        parent_tid_info = f"and linking to parent TID {parent_tid}" if parent_tid != '0x0' else "without a specific parent TID link"
        child_tid_pointer = f"and a child TID pointer at {child_tid}" if child_tid != '0x0' else "without a designated child TID pointer"

        description = (
            f"At {timestamp}, the 'clone' system call was initiated on CPU {cpu_id} by process {pid} (TID {tid}, priority {prio}). "
            f"This call attempts to create a new process or thread {flag_description} {parent_tid_info} {child_tid_pointer}. "
            f"The clone operation is configured with flags {clone_flags}, indicating the specific behaviors and resource sharing between the parent and the new child process."
        )
        return description
    def describe_sched_process_fork(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        parent_tid = row['Contents'].split(', ')[1].split('=')[1]
        parent_pid = row['Contents'].split(', ')[2].split('=')[1]
        parent_ns_inum = row['Contents'].split(', ')[3].split('=')[1]
        child_comm = row['Contents'].split(', ')[4].split('=')[1]
        child_tid = row['Contents'].split(', ')[5].split('=')[1]
        child_pid = row['Contents'].split(', ')[9].split('=')[1]
        child_ns_inum = row['Contents'].split(', ')[10].split('=')[1]

        description = (
            f"At {timestamp}, a process fork occurred on CPU {cpu_id} within the system. "
            f"The parent process, '{child_comm}' (PID {parent_pid}, TID {parent_tid}, namespace {parent_ns_inum}), "
            f"successfully forked to create a new child process named '{child_comm}', "
            f"with PID {child_pid}, TID {child_tid}, and operating within the same namespace (NS inum: {child_ns_inum}). "
            f"This event represents a typical OS operation to create new processes, "
            f"with both parent and child sharing identical command names but distinct process and thread identifiers."
        )
        return description
    def describe_sched_wakeup_new(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        comm = row['Contents'].split(', ')[0].split('=')[1]
        tid = row['Contents'].split(', ')[1].split('=')[1]
        prio = row['Contents'].split(', ')[2].split('=')[1]
        target_cpu = row['Contents'].split(', ')[3].split('=')[1]

        description = (
            f"At {timestamp}, the process '{comm}' with TID {tid} was woken up on CPU {cpu_id} with a priority of {prio}. "
            f"The process is now scheduled to run on target CPU {target_cpu}. This event signifies the activation of a new task, "
            f"typically triggered by the completion of a prior dependent task or by a signal to start a new operation."
        )
        return description
    def describe_syscall_exit_clone(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        ret = row['Contents'].split(', ')[0].split('=')[1]
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']

        description = (
            f"At {timestamp}, the completion of a 'clone' system call was recorded on CPU {cpu_id}. "
            f"This call successfully created a new process with TID {ret}, which is a direct fork of process ID {pid}. "
            f"The new process operates at priority level {prio} and represents a direct attempt to manage or optimize "
            f"task execution through process forking, a common method for multitasking within the kernel."
        )
        return description
    def describe_syscall_entry_execve(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        filename = row['Contents'].split(', ')[0].split('=')[1]
        argv = row['Contents'].split(', ')[1].split('=')[1]
        envp = row['Contents'].split(', ')[2].split('=')[1]

        description = (
            f"At {timestamp}, an 'execve' system call was initiated on CPU {cpu_id} for TID {tid}, priority {prio}. "
            f"The call was made by process {pid} to execute the program '{filename}'. "
            f"Arguments and environment pointers are located at memory addresses {argv} and {envp}, respectively. "
            f"This system call is used to run a new program in the context of the current process, replacing the current executable."
        )
        return description
    def describe_sched_process_exec(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        filename = row['Contents'].split(', ')[0].split('=')[1]
        old_tid = row['Contents'].split(', ')[2].split('=')[1]

        description = (
            f"At {timestamp}, the process with TID {tid} (previously {old_tid}) on CPU {cpu_id}, running under priority {prio}, "
            f"executed the program '{filename}'. This event indicates the replacement of the current running process "
            f"by the specified program, retaining the same process ID {pid} but potentially resetting the execution context."
        )
        return description
    def describe_syscall_exit_execve(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(', ')[0].split('=')[1]

        # Evaluate the success of the syscall
        status = "successfully" if int(ret) == 0 else "with an error"

        description = (
            f"At {timestamp}, the syscall 'execve' executed by process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed {status}. "
            f"This syscall, used for running a new program, returned a status code of {ret}. Successful execution indicates that the program "
            f"has started correctly, replacing the calling process image with a new process image."
        )
        return description
    def describe_syscall_entry_brk(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        brk = row['Contents'].split(', ')[0].split('=')[1]

        # Explaining the purpose of the brk syscall
        action = "requesting the current program break location" if brk == '0' else f"requesting to set the program break to address {brk}"
        description = (
            f"At {timestamp}, a system call to modify the program break was initiated by process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id}. "
            f"The 'brk' system call is {action}. This system call is used to manage the amount of memory allocated to the heap of the process, "
            f"which can grow or shrink based on the needs of the application."
        )
        return description
    def describe_syscall_exit_brk(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(', ')[0].split('=')[1]

        # Explaining the outcome of the brk syscall
        result_description = f"resulting in a new program break location at address {ret}."
        if int(ret) == 0:
            result_description = "but failed to change the program break location."

        description = (
            f"At {timestamp}, the 'brk' system call concluded for process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id}. "
            f"The request {result_description} The 'brk' system call adjusts the end of the data segment to the value specified by brk, "
            f"thereby managing the amount of memory allocated to the process's heap."
        )
        return description
    def describe_syscall_entry_access(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        filename = row['Contents'].split(',')[0].split('=')[1]
        try:
            mode = row['Contents'].split(',')[1].split('=')[1]
        except IndexError:
            mode = 'unknown'


        # Mapping the mode number to its meaning
        modes = {
            '0': 'existence of file',
            '1': 'read permission',
            '2': 'write permission',
            '4': 'execute permission',
            '7': 'read, write, and execute permission'
        }
        mode_description = modes.get(mode, f"special mode {mode}")

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated an 'access' system call to check permissions "
            f"for the file '{filename}'. The operation is attempting to verify the following access mode: {mode_description}. "
            f"This system call is used to determine if the calling process can access the file in the specified way, "
            f"which is important for security checks before actual file operations are performed."
        )
        return description
    def describe_syscall_exit_access(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret_code = row['Contents'].split(',')[0].split('=')[1]

        if int(ret_code) == 0:
            access_result = "successful"
        else:
            access_result = f"failed with error code {ret_code}"

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed an 'access' system call. "
            f"The access check {access_result}. This result is crucial for determining the availability and permissions "
            f"of the file involved in the call, impacting subsequent operations that may depend on this file."
        )
        return description
    def describe_syscall_entry_open(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        parts = row['Contents'].split(', ')
        filename = parts[0].split('=')[1]
        flags = parts[1].split('=')[1]
        mode = parts[2].split('=')[1]

        # Placeholder for mapping flags and mode to human-readable form
        flags_description = "Flags: " + flags  # Extend this to translate flags properly
        mode_description = "Mode: " + mode  # Extend this to translate mode properly

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated an 'open' system call to open the file '{filename}'. "
            f"The call attempts to open the file with {flags_description} and {mode_description}. "
            f"This system call is crucial for file operations, allowing the process to specify how the file should be accessed."
        )
        return description
    def describe_syscall_exit_open(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret_code = row['Contents'].split(',')[0].split('=')[1]

        # Determine the outcome based on the return code
        if int(ret_code) >= 0:
            access_result = f"successfully with file descriptor {ret_code}"
        else:
            error_description = "an unknown error occurred"
            if int(ret_code) == -1:
                error_description = "due to insufficient permissions or the file does not exist"
            elif int(ret_code) == -2:
                error_description = "because the path name is too long"
            access_result = f"failed {error_description}"

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed an 'open' system call. "
            f"The attempt to open the file was {access_result}. This result is critical as it determines the process's ability "
            f"to read from, write to, or execute the file, based on the provided file descriptor. Proper handling of this file descriptor "
            f"is vital for safe and effective file manipulation within the application."
        )
        return description
    def describe_syscall_entry_mprotect(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        contents_parts = row['Contents'].split(', ')
        start = contents_parts[0].split('=')[1]
        len = contents_parts[1].split('=')[1]
        prot = contents_parts[2].split('=')[1]

        # Map protection flags to their meanings
        prot_descriptions = {
            '0': 'no access',
            '1': 'read-only',
            '2': 'write-only',
            '3': 'read-write',
            '4': 'executable',
            '5': 'read-executable',
            '6': 'write-executable',
            '7': 'read-write-executable'
        }
        prot_description = prot_descriptions.get(prot, f"special mode {prot}")

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated an 'mprotect' system call. "
            f"This call is modifying the protection of a memory range starting at {start} with length {len} bytes. "
            f"The requested protection level is set to '{prot_description}'. This syscall is crucial for managing memory protection "
            f"rights for the application's memory space, ensuring memory access rights are aligned with the application's processing requirements."
        )
        return description
    def describe_syscall_exit_mprotect(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        contents = row['Contents'].split(', ')
        ret_code = contents[0].split('=')[1]  # Correctly extract the return value
        source = row['Source']  # Extract the source file information

        # Check the return code to determine the result of the syscall
        if int(ret_code) == 0:
            result_description = "successfully modified the memory protection settings."
        else:
            result_description = f"failed with error code {ret_code}, indicating an issue with the parameters or permissions."

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed an 'mprotect' system call. "
            f"The attempt to change memory protection {result_description} This operation, processed in the source file '{source}', "
            f"is critical for controlling access to the application's memory, ensuring the security and proper functioning of memory usage."
        )
        return description
    def describe_syscall_exit_unknown(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        id_ = row['Contents'].split(',')[0].split('=')[1]
        ret_code = row['Contents'].split(',')[1].split('=')[1]

        args = [
            row['Contents'].split('args._args[0]=')[1].split(',')[0],
            row['Contents'].split('args._args[1]=')[1].split(',')[0],
            row['Contents'].split('args._args[2]=')[1].split(',')[0],
            row['Contents'].split('args._args[3]=')[1].split(',')[0],
            row['Contents'].split('args._args[4]=')[1].split(',')[0],
            row['Contents'].split('args._args[5]=')[1].split(',')[0]
        ]

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed an unknown system call (ID: {id_}). "
            f"The call returned {ret_code}, with arguments {args}. The details of this syscall are not fully known, indicating either "
            f"an undocumented syscall or one that is less commonly used. The return value and arguments provide some context about the operation's intent."
        )
        return description
    def describe_syscall_entry_munmap(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        contents = row['Contents']

        # Extract the address and length from the contents
        addr = contents.split('addr=')[1].split(',')[0]
        length = contents.split('len=')[1].split(',')[0]
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'munmap' system call "
            f"to unmap memory starting at address {addr} with a length of {length} bytes. This system call is used to release "
            f"memory previously mapped into the process's address space, which is critical for managing system memory efficiently and preventing memory leaks. "
            f"The operation is managed by the kernel module defined in {source}."
        )
        return description
    def describe_syscall_exit_munmap(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret_code = row['Contents'].split(',')[0].split('=')[1]  # Safely extracting the return code
        source = row['Source']

        if int(ret_code) == 0:
            result = "successfully"
        else:
            result = f"failed with error code {ret_code}"

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'munmap' system call. "
            f"The operation {result} unmapped the memory, which is crucial for releasing resources and managing memory "
            f"efficiently within the system. The call was managed by the kernel module located at {source}."
        )
        return description
    def describe_syscall_entry_getpid(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'getpid' system call. "
            f"This system call is used to retrieve the process ID of the calling process. It's a straightforward call with no arguments, "
            f"reflecting the process's request to obtain its own identifier. The operation is handled by the kernel module located at {source}, "
            f"which is integral for managing process-specific data and interactions within the system."
        )
        return description
    def describe_syscall_exit_getpid(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret_code = row['Contents'].split('=')[1].split(',')[0]  # Extracts the return code correctly
        source = row['Source']

        description = (
            f"At {timestamp}, the completion of a 'getpid' system call was recorded for process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id}. "
            f"The system call returned a process ID of {ret_code}, which is expected as 'getpid' should return the caller's PID. "
            f"This execution path through the system, specifically managed by the kernel code at {source}, confirms the successful retrieval of the process ID. "
            f"This identifier is crucial for the process's interactions with the system, particularly for resource management and security purposes."
        )
        return description
    def describe_syscall_entry_geteuid(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'geteuid' system call. "
            f"This system call is used to retrieve the effective user ID of the calling process. The effective user ID determines "
            f"the privileges for the process, especially what resources it can access on the system. This operation is handled by "
            f"the kernel at the source code location {source}, which is crucial for enforcing security and permission mechanisms in the operating system."
        )
        return description
    def describe_syscall_exit_geteuid(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(',')[0].split('=')[1]  # Extract the return value from the contents
        source = row['Source']

        euid_description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} successfully completed the 'geteuid' system call. "
            f"The call returned an effective user ID (EUID) of {ret}. This EUID is used by the operating system to determine the "
            f"privileges of the process for accessing system resources. The operation, tracked in the kernel at {source}, is critical for "
            f"enforcing security protocols based on user identities."
        )
        return euid_description
    def describe_syscall_entry_getppid(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'getppid' system call. "
            f"This system call is used to retrieve the process ID (PID) of the parent process. Understanding the parent-child process "
            f"relationship is crucial for managing process hierarchies within the operating system. The call was handled in the "
            f"system context defined in {source}, ensuring the process can correctly identify and interact with its parent."
        )
        return description
    def describe_syscall_exit_getppid(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret_value = row['Contents'].split('=')[1].split(',')[0]  # Correctly extracting the return value
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'getppid' system call, "
            f"successfully retrieving the parent process ID (PPID), which is {ret_value}. This information is essential for the process "
            f"to understand its place within the system's process hierarchy. The operation was managed according to the "
            f"protocol outlined in {source}, ensuring accurate and secure process management."
        )
        return description
    def describe_syscall_entry_newstat(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        filename = row['Contents'].split('=')[1].split(',')[0]  # Correctly extracting the filename
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'newstat' system call to retrieve statistics "
            f"for the file '{filename}'. This system call is essential for obtaining detailed information about the file, "
            f"such as size, permissions, and modification times. The file operations and metadata retrieval are managed according to the "
            f"protocol outlined in {source}, ensuring accurate and secure access to filesystem data."
        )
        return description
    def describe_syscall_exit_newstat(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret_code, statbuf = row['Contents'].split(', ')[0].split('=')[1], row['Contents'].split(', ')[1].split('=')[1]
        source = row['Source']

        if int(ret_code) == 0:
            result = "successfully"
        else:
            result = f"with error code {ret_code}"

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'newstat' system call {result}. "
            f"The 'stat' structure is located at address {statbuf}, containing detailed information about the file. This system call is "
            f"essential for retrieving file metadata, ensuring proper file management and security checks. The execution details are managed according to "
            f"the protocol outlined in {source}."
        )
        return description
    def describe_syscall_entry_fcntl(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extract values safely
        parts = row['Contents'].split(', ')
        fd = parts[0].split('=')[1]
        cmd = parts[1].split('=')[1]
        arg = parts[2].split('=')[1]

        # Mapping command codes directly within the function
        commands = {
            '0': 'F_DUPFD',  # Duplicate file descriptor
            '1': 'F_GETFD',  # Get file descriptor flags
            '2': 'F_SETFD',  # Set file descriptor flags
            # Add more command descriptions as needed
        }
        command_description = commands.get(cmd, f"Unknown command {cmd}")

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'fcntl' system call with file descriptor {fd}. "
            f"The command '{command_description}' with argument {arg} is being processed. This system call is used for manipulating file descriptors and is "
            f"fundamental for controlling file operations within the process. Detailed file control operations are implemented as defined in {source}."
        )
        return description
    def describe_syscall_exit_fcntl(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extract values correctly using split
        parts = row['Contents'].split(', ')
        ret = parts[0].split('=')[1]
        arg = parts[1].split('=')[1]

        # Interpret return value
        if int(ret) == 0:
            result = "successful"
        else:
            result = f"failed with error code {ret}"

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'fcntl' system call. "
            f"The operation returned with {result}, affecting the argument {arg}. This system call typically involves manipulation "
            f"of file descriptor flags or capabilities, crucial for controlling how files are accessed by the process. Detailed behavior "
            f"and implications are outlined in the source file {source}."
        )
        return description
    def describe_syscall_entry_pipe(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'pipe' system call. "
            f"This system call is used to create a pair of file descriptors pointing to a pipe object, which can be used "
            f"to enable inter-process communication (IPC) between two or more processes. This operation is critical for "
            f"processes that need to communicate or share data securely and efficiently. Referenced source file: {source}."
        )
        return description
    def describe_syscall_exit_pipe(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']
        ret = row['Contents'].split(',')[0].split('=')[1]  # Extract return value directly
        fildes_0 = row['Contents'].split('fildes._fildes[0]=')[1].split(',')[0]  # Extract first file descriptor
        fildes_1 = row['Contents'].split('fildes._fildes[1]=')[1].split(',')[0]  # Extract second file descriptor

        success_status = "successfully" if int(ret) == 0 else "unsuccessfully"

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'pipe' system call {success_status}. "
            f"File descriptors {fildes_0} and {fildes_1} were allocated for inter-process communication. This call establishes a unidirectional "
            f"data channel that processes can use to exchange data securely and efficiently. Referenced source file: {source}."
        )
        return description
    def describe_syscall_entry_dup2(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        oldfd = row['Contents'].split('oldfd=')[1].split(',')[0]  # Extract old file descriptor
        newfd = row['Contents'].split('newfd=')[1].split(',')[0]  # Extract new file descriptor
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'dup2' system call "
            f"to duplicate file descriptor {oldfd} into file descriptor {newfd}. This operation allows the process "
            f"to redirect output or input streams, commonly used in shell command pipelines and redirections. "
            f"Referenced source file: {source}."
        )
        return description
    def describe_syscall_exit_dup2(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret_code = row['Contents'].split(',')[0].split('=')[1]  # Extract return code
        source = row['Source']

        if int(ret_code) == -1:
            result_description = "failed due to an error"
        else:
            result_description = f"successfully duplicated to file descriptor {ret_code}"

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'dup2' system call. "
            f"The attempt to duplicate the file descriptor {result_description}. "
            f"Referenced source file: {source}."
        )
        return description
    def describe_syscall_entry_chdir(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        filename = row['Contents'].split(',')[0].split('=')[1]  # Extract filename
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'chdir' system call "
            f"to change the current working directory to '{filename}'. This operation is essential for tasks that require "
            f"working within a specific directory structure. Referenced source file: {source}."
        )
        return description
    def describe_syscall_exit_chdir(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret_code = row['Contents'].split(',')[0].split('=')[1]  # Extract return code
        source = row['Source']

        # Determine the result of the chdir operation
        if int(ret_code) == 0:
            result = "successfully changed the current working directory."
        else:
            result = f"failed to change the directory with error code {ret_code}."

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'chdir' system call. "
            f"The attempt to change the directory {result} Referenced source file: {source}."
        )
        return description
    def describe_syscall_entry_getdents(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        contents = row['Contents'].split(',')
        fd = contents[0].split('=')[1]
        count = contents[1].split('=')[1]
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'getdents' system call "
            f"using file descriptor {fd} to read up to {count} directory entries. This call is typically used to read the contents "
            f"of a directory, enabling the process to retrieve detailed information about each file in the directory. "
            f"Referenced source file: {source}."
        )
        return description
    def describe_syscall_exit_getdents(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        contents = row['Contents'].split(', ')
        ret = contents[0].split('=')[1]
        dirent = contents[1].split('=')[1]
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'getdents' system call. "
            f"The operation returned {ret} entries, accessing directory entries starting at memory address {dirent}. "
            f"This call is commonly used to read directory contents for file management operations. "
            f"Referenced source file: {source}."
        )
        return description
    def describe_syscall_entry_faccessat(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        contents = row['Contents'].split(', ')
        dfd = contents[0].split('=')[1]
        filename = contents[1].split('=')[1]
        mode = contents[2].split('=')[1]
        source = row['Source']

        # Mapping the mode to a more human-readable format
        mode_description = {
            '0': 'exist',
            '1': 'read',
            '2': 'write',
            '4': 'execute',
            '7': 'read, write, and execute'
        }.get(mode, "unknown")

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'faccessat' system call. "
            f"This call checks if the file '{filename}' has '{mode_description}' permissions. The directory file descriptor (dfd) is {dfd}. "
            f"This operation is essential for validating access rights to files before performing operations that require specific permissions. "
            f"Referenced source file: {source}."
        )
        return description
    def describe_syscall_exit_faccessat(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret = row['Contents'].split(',')[0].split('=')[1]  # Extract return value correctly

        if int(ret) == 0:
            result = "successful"
        else:
            result = f"failed with error code {ret}"

        source = row['Source']

        description = (
            f"At {timestamp}, the 'faccessat' system call executed by process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} "
            f"completed and was {result}. This call verifies access permissions for a file or directory. "
            f"Referenced source file: {source}."
        )
        return description
    def describe_syscall_entry_getuid(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        description = (
            f"At {timestamp}, the process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'getuid' system call. "
            f"This call retrieves the user ID of the calling process. The operation is being executed as part of the code at {source}."
        )
        return description
    def describe_syscall_exit_getuid(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        uid = row['Contents'].split(',')[0].split('=')[1]  # Extract the UID returned by the syscall
        source = row['Source']

        description = (
            f"At {timestamp}, the process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed the 'getuid' system call. "
            f"The system call returned a user ID of {uid}, indicating the unique identifier of the user associated with the process. "
            f"The operation was executed as part of the code at {source}."
        )
        return description
    def describe_syscall_entry_getgid(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'getgid' system call. "
            f"This system call retrieves the group ID of the user currently executing the process. "
            f"Initiating such calls is a common operation in systems for access control and in managing user group permissions. "
            f"Code executing this call is located at {source}."
        )
        return description
    def describe_syscall_exit_getgid(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        ret_value = row['Contents'].split(',')[0].split('=')[1]  # Extracts return value from Contents
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'getgid' system call with a return value of {ret_value}. "
            f"This value represents the group ID associated with the user executing the process. "
            f"The successful retrieval of the group ID confirms user group membership and can be used for managing access permissions. "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_entry_mkdir(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the pathname and mode directly from the contents
        contents = row['Contents'].split(', ')
        data = {k: v for item in contents for k, v in [item.split('=')]}

        pathname = data['pathname']
        mode = data['mode']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'mkdir' system call to create a new directory at '{pathname}'. "
            f"The directory is being created with mode settings {mode} (octal: {oct(int(mode))}). This action configures the accessibility and permissions of the new directory. "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_exit_mkdir(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extract the return code and context information from the contents
        contents = row['Contents'].split(', ')
        data = {k: v for item in contents for k, v in [item.split('=')]}

        ret_code = data['ret']
        result = "Success" if int(ret_code) == 0 else "Failure"

        description = (
            f"At {timestamp}, the 'mkdir' system call initiated by process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed with a return code of {ret_code}. "
            f"This indicates a {result.lower()} in creating the specified directory. "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_entry_set_tid_address(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the tidptr directly from the contents
        contents = row['Contents'].split(', ')
        data = {k: v for item in contents for k, v in [item.split('=')]}

        tidptr = data['tidptr']

        description = (
            f"At {timestamp}, process with PID {pid} and thread ID {tid}, running on CPU {cpu_id} with priority {prio}, called the 'set_tid_address' system call. "
            f"The system call sets the address where the kernel can store the thread ID of the exiting thread. This is particularly important for robust thread synchronization and cleanup operations. "
            f"The address provided for this operation is {tidptr}. This call is essential for managing thread lifecycles effectively and is used by various threading libraries to ensure proper resource deallocation on thread termination. "
            f"The system call was triggered from the source located at {source}."
        )
        return description
    def describe_syscall_exit_set_tid_address(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the return value directly from the contents
        ret = row['Contents'].split(',')[0].split('=')[1]

        description = (
            f"At {timestamp}, the 'set_tid_address' system call completed on CPU {cpu_id} for process {pid} with thread ID {tid}, running at priority {prio}. "
            f"The system call returned {ret}, which is the thread ID of the calling process or zero if the call was unsuccessful. "
            f"This system call is typically used to manage thread lifecycles and synchronization, allowing the kernel to clean up thread-specific resources upon thread exit. "
            f"Origin of the call: {source}."
        )
        return description
    def describe_syscall_entry_set_robust_list(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the head address and length directly from the contents
        contents = row['Contents'].split(', ')
        data = {k: v for item in contents for k, v in [item.split('=')]}

        head = data['head']
        length = data['len']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'set_robust_list' system call with head pointer at {head} and list length {length} bytes. "
            f"This system call is used to set up a list of futexes that are to be managed automatically by the kernel at the thread's exit, ensuring that no locks remain held by the exiting thread. "
            f"The operation was triggered from {source}."
        )
        return description
    def describe_syscall_exit_set_robust_list(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extract the return value from the Contents
        ret = int(row['Contents'].split(', ')[0].split('=')[1])  # Assuming 'ret=...' is always first in Contents

        # Basic description framework
        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed the 'set_robust_list' system call. "
            f"Source of this system call is located at {source}. "
        )

        # Conditional extension of the description based on the return value
        if ret == 0:
            description += "The operation was successful, indicating that the robust list was set correctly without errors."
        else:
            description += f"The operation failed with a return code of {ret}, indicating a potential error or invalid operation parameters."

        return description
    def describe_syscall_entry_getrlimit(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']
        resource = row['Contents'].split(',')[0].split('=')[1]  # Extracting the resource number from Contents

        # Expanded resource descriptions based on typical resource IDs in Linux
        resource_map = {
            '0': 'RLIMIT_CPU',  # CPU time in seconds
            '1': 'RLIMIT_FSIZE',  # Maximum filesize
            '2': 'RLIMIT_DATA',  # Max data size
            '3': 'RLIMIT_STACK',  # Max stack size
            '4': 'RLIMIT_CORE',  # Max core file size
            '5': 'RLIMIT_RSS',  # Max resident set size
            '6': 'RLIMIT_NPROC',  # Max number of processes
            '7': 'RLIMIT_NOFILE',  # Max number of open files
            '8': 'RLIMIT_MEMLOCK',  # Max locked-in-memory address space
            '9': 'RLIMIT_AS',  # Address space limit
            '10': 'RLIMIT_LOCKS',  # Maximum file locks
            '11': 'RLIMIT_SIGPENDING',  # Max number of pending signals
            '12': 'RLIMIT_MSGQUEUE',  # Max bytes in POSIX message queues
            '13': 'RLIMIT_NICE',  # Max nice priority allowed to raise to
            '14': 'RLIMIT_RTPRIO',  # Max realtime priority
            '15': 'RLIMIT_RTTIME'  # Timeout for realtime tasks in microseconds
        }

        resource_name = resource_map.get(resource, 'Unknown Resource')

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'getrlimit' system call to query the resource limits for {resource_name}. "
            f"This system call checks the maximum size that a resource can take, such as maximum file size, memory usage, or number of open files. "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_exit_getrlimit(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']
        ret = int(row['Contents'].split(',')[0].split('=')[1])  # Extracting the return value from Contents
        rlim = row['Contents'].split(',')[1].split('=')[1]  # Extracting the rlim address from Contents

        if ret == 0:
            description = (
                f"At {timestamp}, the 'getrlimit' system call executed by process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed successfully. "
                f"The limits for the requested resource are stored at memory address {rlim}. This address points to the structure containing the soft and hard limits. "
                f"Source of this system call is located at {source}."
            )
        else:
            description = (
                f"At {timestamp}, the 'getrlimit' system call executed by process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} failed with a return code of {ret}. "
                f"This indicates a problem retrieving the resource limits. Ensure the requested resource identifier is valid and the process has adequate permissions to access this information. "
                f"Source of this system call is located at {source}."
            )

        return description
    def describe_syscall_entry_getcwd(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the size from the contents
        size = row['Contents'].split(',')[0].split('=')[1]

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'getcwd' system call to retrieve the current working directory. "
            f"The buffer size allocated for this operation is {size} bytes. This call will return the absolute path of the current working directory stored in the provided buffer. "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_exit_getcwd(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the return value and buffer address from the contents
        contents = row['Contents'].split(', ')
        ret = contents[0].split('=')[1]
        buf = contents[1].split('=')[1]

        # Determine the outcome based on the return value
        if int(ret) > 0:
            description = (
                f"At {timestamp}, the 'getcwd' system call completed successfully on CPU {cpu_id} for process {pid} (TID {tid}, priority {prio}). "
                f"The call returned {ret} bytes, indicating the size of the current working directory path stored at memory address {buf}. "
                f"This successful call indicates the current directory path could be retrieved within the allocated buffer size."
            )
        else:
            description = (
                f"At {timestamp}, the 'getcwd' system call failed on CPU {cpu_id} for process {pid} (TID {tid}, priority {prio}). "
                f"The system call returned an error code of {ret}, indicating a failure to retrieve the current working directory. "
                f"This error could be due to insufficient buffer size or other system-level constraints."
            )

        return description
    def describe_syscall_entry_newlstat(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting filename from the contents
        contents = row['Contents'].split(', ')
        filename = contents[0].split('=')[1]

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} invoked the 'newlstat' system call to retrieve status information about the file at '{filename}'. "
            f"This system call is used to get details such as file size, permissions, and modification time without following symbolic links. "
            f"The request originated from the code reference at {source}."
        )
        return description
    def describe_syscall_exit_newlstat(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']
        ret = int(row['Contents'].split(', ')[0].split('=')[1])
        statbuf_address = row['Contents'].split(', ')[1].split('=')[1]

        if ret == 0:
            description = f"At {timestamp}, the 'newlstat' system call completed successfully for process {pid} on CPU {cpu_id}. The file's status information was stored at address {statbuf_address}."
        else:
            error_message = "File not found" if ret == -2 else "Unknown error"
            description = f"At {timestamp}, the 'newlstat' system call by process {pid} failed with return code {ret} ({error_message}). No file status information was retrieved."

        description += f" The operation was executed on thread ID {tid} with priority {prio}, sourced from {source}."
        return description
    def describe_syscall_entry_futex(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting values from the 'Contents' field
        contents = row['Contents'].split(', ')
        data = {k: v for item in contents for k, v in [item.split('=')]}

        uaddr = data['uaddr']
        op = data['op']
        val = data['val']
        utime = data['utime']
        uaddr2 = data['uaddr2']
        val3 = data['val3']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'futex' system call. "
            f"The operation will perform a futex operation on the user-space address {uaddr}. The operation code (op) is {op}, "
            f"with a value of {val}, and a timeout of {utime}. Additionally, the second user-space address is {uaddr2}, and the third value is {val3}. "
            f"This system call is used for fast user-space locking, allowing processes to wait for and wake up from specific conditions. "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_exit_futex(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting values from the 'Contents' field
        contents = row['Contents'].split(', ')
        data = {k: v for item in contents for k, v in [item.split('=')]}

        ret = data['ret']
        uaddr = data['uaddr']
        uaddr2 = data['uaddr2']

        if int(ret) == 0:
            ret_description = "The futex operation completed successfully."
        else:
            ret_description = f"The futex operation failed with error code {ret}."

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'futex' system call. "
            f"The operation was performed on the user-space address {uaddr} with a second user-space address {uaddr2}. "
            f"{ret_description} "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_entry_pipe2(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting values from the 'Contents' field
        contents = row['Contents'].split(', ')
        data = {k: v for item in contents for k, v in [item.split('=')]}

        flags = data['flags']

        # Convert flags to hexadecimal for better readability in some contexts
        flags_hex = hex(int(flags))

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'pipe2' system call. "
            f"This call aims to create a pipe, which is a unidirectional data channel used for inter-process communication (IPC). "
            f"The call includes flags set to {flags} (hex: {flags_hex}), which alter the default behavior of the pipe. "
            f"These flags could be used to set properties such as non-blocking mode (O_NONBLOCK), close-on-exec (O_CLOEXEC), or others depending on the value specified. "
            f"The exact nature of these flags provides insights into the intended behavior of the pipe for this specific process. "
            f"The system call source is identified at {source}."
        )
        return description
    def describe_syscall_exit_pipe2(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting values from the 'Contents' field
        contents = row['Contents'].split(', ')
        data = {k: v for item in contents for k, v in [item.split('=')]}

        ret = data['ret']
        fildes_0 = data['fildes._fildes[0]']
        fildes_1 = data['fildes._fildes[1]']

        if int(ret) == 0:
            result_description = (
                f"The call was successful, creating a pipe with file descriptors {fildes_0} for reading and {fildes_1} for writing."
            )
        else:
            result_description = (
                f"However, the call failed with a return value of {ret}, indicating an error occurred."
            )

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'pipe2' system call. "
            f"{result_description} "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_entry_socket(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting values from the 'Contents' field
        contents = row['Contents'].split(', ')
        data = {k: v for item in contents for k, v in [item.split('=')]}

        family = data['family']
        type_ = data['type']
        protocol = data['protocol']

        family_mapping = {
            "1": "AF_UNIX (local communication)",
            "2": "AF_INET (IPv4)",
            "10": "AF_INET6 (IPv6)",
            "17": "AF_PACKET (low-level packet interface)",
            "3": "AF_AX25 (Amateur radio AX.25 protocol)",
            "4": "AF_IPX (IPX - Novell protocols)",
            "5": "AF_APPLETALK (Appletalk DDP)",
            "6": "AF_NETROM (Amateur radio NET/ROM)",
            "7": "AF_BRIDGE (Multiprotocol bridge)",
            "8": "AF_ATMPVC (ATM PVCs)",
            "9": "AF_X25 (ITU-T X.25 / ISO-8208 protocol)",
            "11": "AF_ROSE (Amateur Radio X.25 PLP)",
            "12": "AF_DECnet (Reserved for DECnet project)",
            "13": "AF_NETBEUI (Reserved for 802.2LLC project)",
            "14": "AF_SECURITY (Security callback pseudo AF)",
            "15": "AF_KEY (PF_KEY key management API)",
            "16": "AF_NETLINK (Linux netlink)",
            "18": "AF_ASH (Ash)",
            "19": "AF_ECONET (Acorn Econet)",
            "20": "AF_ATMSVC (ATM SVCs)",
            "21": "AF_RDS (RDS sockets)",
            "22": "AF_SNA (Linux SNA Project)",
            "23": "AF_IRDA (IrDA sockets)",
            "24": "AF_PPPOX (PPP over X sockets)",
            "25": "AF_WANPIPE (WANPIPE API sockets)",
            "26": "AF_LLC (Linux LLC)",
            "27": "AF_IB (InfiniBand)",
            "28": "AF_MPLS (MPLS)",
            "29": "AF_CAN (Controller Area Network)",
            "30": "AF_TIPC (TIPC sockets)",
            "31": "AF_BLUETOOTH (Bluetooth sockets)",
            "32": "AF_IUCV (IUCV sockets)",
            "33": "AF_RXRPC (RxRPC sockets)",
            "34": "AF_ISDN (mISDN sockets)",
            "35": "AF_PHONET (Phonet sockets)",
            "36": "AF_IEEE802154 (IEEE 802.15.4 sockets)",
            "37": "AF_CAIF (CAIF sockets)",
            "38": "AF_ALG (Algorithm sockets)",
            "39": "AF_NFC (NFC sockets)",
            "40": "AF_VSOCK (vSockets)",
            "41": "AF_KCM (Kernel Connection Multiplexor)",
            "42": "AF_QIPCRTR (Qualcomm IPC Router)",
            "43": "AF_SMC (smc sockets)",
            "44": "AF_XDP (XDP sockets)",
            # Add other family mappings as needed
        }

        type_mapping = {
            "1": "SOCK_STREAM (reliable, connection-based byte streams)",
            "2": "SOCK_DGRAM (connectionless, unreliable datagrams of fixed maximum length)",
            "3": "SOCK_RAW (raw network protocol access)",
            "4": "SOCK_RDM (reliable datagram layer that does not guarantee ordering)",
            "5": "SOCK_SEQPACKET (sequenced, reliable, connection-based, two-way transmission data path)",
            "6": "SOCK_DCCP (Datagram Congestion Control Protocol)",
            "10": "SOCK_PACKET (low-level packet interface)",
            # Add other type mappings as needed
        }

        family_description = family_mapping.get(family, f"Unknown family ({family})")
        type_description = type_mapping.get(type_, f"Unknown type ({type_})")

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'socket' system call. "
            f"The socket was created with family {family_description}, type {type_description}, and protocol {protocol}. "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_exit_socket(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting values from the 'Contents' field
        contents = row['Contents'].split(', ')
        data = {k: v for item in contents for k, v in [item.split('=')]}

        ret = data['ret']

        if ret == '0':
            ret_description = "successfully created a new socket."
        else:
            ret_description = f"encountered an error with code {ret} while attempting to create a new socket."

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} exited a 'socket' system call and {ret_description} "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_entry_connect(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting values from the 'Contents' field
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                k, v = item.split('=', 1)
                data[k] = v

        # Extract the required fields from the data dictionary
        family = data.get('family')
        type = data.get('type')
        protocol = data.get('protocol')

        family_mapping = {
            '1': 'AF_UNIX',
            '2': 'AF_INET',
            '10': 'AF_INET6',
            '16': 'AF_NETLINK',
            '17': 'AF_PACKET',
            '3': 'AF_AX25',
            '4': 'AF_IPX',
            '5': 'AF_APPLETALK',
            '6': 'AF_NETROM',
            '8': 'AF_X25',
            '9': 'AF_INET6',
            '11': 'AF_ROSE',
            '12': 'AF_DECnet',
            '13': 'AF_NETBEUI',
            '14': 'AF_SECURITY',
            '15': 'AF_KEY',
            # Add other family mappings as needed
        }

        type_mapping = {
            '1': 'SOCK_STREAM',
            '2': 'SOCK_DGRAM',
            '3': 'SOCK_RAW',
            '4': 'SOCK_RDM',
            '5': 'SOCK_SEQPACKET',
            '6': 'SOCK_DCCP',
            '10': 'SOCK_PACKET',
            '526337': 'SOCK_DGRAM | SOCK_NONBLOCK',
            '526385': 'SOCK_STREAM | SOCK_NONBLOCK',
            '2050': 'SOCK_RAW | SOCK_NONBLOCK',
            '2051': 'SOCK_RDM | SOCK_NONBLOCK',
            # Add other type mappings as needed
        }

        family_str = family_mapping.get(family, family)
        type_str = type_mapping.get(type, type)

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} made a 'connect' system call. "
            f"The socket was configured with family '{family_str}', type '{type_str}', and protocol '{protocol}'. "
            f"Source of this system call is located at {source}."
        )

        return description
    def describe_syscall_exit_connect(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting values from the 'Contents' field
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                k, v = item.split('=', 1)
                data[k] = v

        ret = data.get('ret')

        # Generate different descriptions based on the return value
        if ret == '0':
            result_str = "The connect system call was successful, indicating that the connection to the remote socket was established without any errors."
        else:
            error_code = ret  # Here, you could map error codes to human-readable strings if desired
            result_str = f"The connect system call failed with an error code {error_code}. This indicates that the connection to the remote socket could not be established."

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'connect' system call. "
            f"{result_str} "
            f"Source of this system call is located at {source}."
        )

        return description
    def describe_syscall_entry_newuname(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'newuname' system call. "
            f"This system call is used to get information about the current kernel, such as the kernel name, node name, kernel release, kernel version, machine, and domain name. "
            f"The source of this system call is located at {source}."
        )

        return description
    def describe_syscall_exit_newuname(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the ret and name from the contents
        contents = row['Contents'].split(', ')
        data = {item.split('=')[0]: item.split('=')[1] for item in contents if '=' in item}

        ret = int(data['ret'])
        name = data['name']

        if ret == 0:
            description = (
                f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} successfully completed a 'newuname' system call. "
                f"The system call returned information about the current kernel, and the results were stored in the structure located at address {name}. "
                f"Source of this system call is located at {source}."
            )
        else:
            description = (
                f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} attempted a 'newuname' system call, but it failed with return code {ret}. "
                f"This indicates an error occurred during the system call, preventing the retrieval of the kernel information. "
                f"Source of this system call is located at {source}."
            )

        return description
    def describe_syscall_entry_poll(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the ufds, nfds, and timeout_msecs from the contents
        contents = row['Contents'].split(', ')
        data = {item.split('=')[0]: item.split('=')[1] for item in contents if '=' in item}

        ufds = data['ufds']
        nfds = data['nfds']
        timeout_msecs = data['timeout_msecs']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'poll' system call. "
            f"This call checks for events on the file descriptors specified in the array at address {ufds}, which contains {nfds} descriptors. "
            f"The poll will wait for {timeout_msecs} milliseconds before timing out. "
            f"The source of this system call is located at {source}."
        )
        return description
    def describe_syscall_exit_poll(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the return value and ufds from the contents
        contents = row['Contents'].split(', ')
        data = {item.split('=')[0]: item.split('=')[1] for item in contents if '=' in item}

        ret = data['ret']
        ufds = data['ufds']

        # Generating a detailed description based on the return value
        if int(ret) >= 0:
            description = (
                f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'poll' system call. "
                f"The call monitored file descriptors in the array at address {ufds}. "
                f"It returned {ret}, indicating the number of file descriptors with events to report. "
                f"The source of this system call is located at {source}."
            )
        else:
            description = (
                f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} encountered an error during a 'poll' system call. "
                f"The call attempted to monitor file descriptors in the array at address {ufds}, but it failed with a return value of {ret}. "
                f"The source of this system call is located at {source}."
            )

        return description
    def describe_syscall_entry_sendmmsg(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the parameters from the contents
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        fd = data.get('fd')
        mmsg = data.get('mmsg')
        vlen = data.get('vlen')
        flags = data.get('flags')

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'sendmmsg' system call. "
            f"This call attempts to send multiple messages on socket file descriptor {fd}. "
            f"The messages are located at address {mmsg} and the call attempts to send up to {vlen} messages. "
            f"The flags used for this operation are {flags}. "
            f"The source of this system call is located at {source}."
        )
        return description
    def describe_syscall_exit_sendmmsg(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the return value from the contents
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        ret = data.get('ret')

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'sendmmsg' system call. "
            f"The call resulted in a return value of {ret}, indicating that {ret} messages were successfully sent. "
            f"The source of this system call is located at {source}."
        )

        return description
    def describe_syscall_entry_recvfrom(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the fd, size, flags, and addr_len from the contents
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        fd = data.get('fd')
        size = data.get('size')
        flags = data.get('flags')
        addr_len = data.get('addr_len')

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'recvfrom' system call. "
            f"The call is intended to receive data from file descriptor {fd}, with a maximum size of {size} bytes. "
            f"The flags used for this call are {flags}, and the address length is specified as {addr_len}. "
            f"The source of this system call is located at {source}."
        )

        return description
    def describe_syscall_exit_recvfrom(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the ret, ubuf, addr, and addr_len from the contents
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        ret = data.get('ret')
        ubuf = data.get('ubuf')
        addr = data.get('addr')
        addr_len = data.get('addr_len')

        if int(ret) >= 0:
            description = (
                f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'recvfrom' system call. "
                f"The call received {ret} bytes of data into the user buffer located at address {ubuf}. "
                f"The source address of the received data is stored at address {addr}, with the length of the address stored at {addr_len}. "
                f"The source of this system call is located at {source}."
            )
        else:
            description = (
                f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} attempted a 'recvfrom' system call, but it failed with return value {ret}. "
                f"The user buffer was located at address {ubuf}, and the source address of the attempted received data was stored at address {addr}, with the length of the address stored at {addr_len}. "
                f"The source of this system call is located at {source}."
            )

        return description
    def describe_syscall_entry_fadvise64(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the fd, offset, len, and advice from the contents
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        fd = data.get('fd')
        offset = data.get('offset')
        length = data.get('len')
        advice = data.get('advice')

        # Mapping advice values to human-readable descriptions
        advice_mapping = {
            '0': 'POSIX_FADV_NORMAL',
            '1': 'POSIX_FADV_RANDOM',
            '2': 'POSIX_FADV_SEQUENTIAL',
            '3': 'POSIX_FADV_WILLNEED',
            '4': 'POSIX_FADV_DONTNEED',
            '5': 'POSIX_FADV_NOREUSE'
        }

        advice_description = advice_mapping.get(advice, 'Unknown advice')

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'fadvise64' system call. "
            f"The call was made on file descriptor {fd}, starting at offset {offset} for a length of {length} bytes. "
            f"The advice provided was {advice_description} ({advice}), which guides the kernel's behavior in managing the file's cache. "
            f"The source of this system call is located at {source}."
        )

        return description
    def describe_syscall_exit_fadvise64(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the ret value from the contents
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        ret = data.get('ret')

        # Description based on ret value
        if ret == '0':
            ret_description = "The system call executed successfully."
        else:
            ret_description = f"The system call failed with return value {ret}."

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'fadvise64' system call. "
            f"{ret_description} "
            f"The source of this system call is located at {source}."
        )

        return description
    def describe_syscall_entry_getsockopt(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the fd, level, optname, and optlen directly from the contents
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        fd = data['fd']
        level = data['level']
        optname = data['optname']
        optlen = data['optlen']

        # Level and optname mapping for better description
        level_map = {
            '1': 'SOL_SOCKET'
        }
        optname_map = {
            '4': 'SO_REUSEADDR'
        }

        level_description = level_map.get(level, f"Unknown level ({level})")
        optname_description = optname_map.get(optname, f"Unknown option ({optname})")

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'getsockopt' system call on file descriptor {fd}. "
            f"This call queries socket options at the {level_description} level, specifically the {optname_description} option. "
            f"The expected size of the option value to retrieve is {optlen} bytes. "
            f"Source of this system call is located at {source}."
        )

        return description
    def describe_syscall_exit_getsockopt(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the return value, option value, and option length directly from the contents
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        ret = data['ret']
        optval = data['optval']
        optlen = data['optlen']

        # Describe the result based on the return value
        if ret == "0":
            result_description = "successfully retrieved"
        else:
            result_description = f"failed with error code {ret}"

        description = (
            f"At {timestamp}, the process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'getsockopt' system call. "
            f"The operation {result_description}. The option value is stored at memory address {optval} with a length of {optlen} bytes. "
            f"Source of this system call is located at {source}."
        )

        return description
    def describe_syscall_entry_sendto(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting buffer, length, flags, address, and address length from the contents
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        buff = data['buff']
        length = data['len']
        flags = data['flags']
        addr = data['addr']
        addr_len = data['addr_len']

        # Constructing address info
        if addr == '0' or not addr_len:
            address_info = "no destination address specified"
        else:
            address_info = f"to destination address at memory location {addr} with a length of {addr_len} bytes"

        # Constructing flag info
        flag_description = "with flags" if flags != '0' else "with no flags"

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'sendto' system call. "
            f"This call attempts to send data from buffer at {buff} of length {length} bytes {flag_description} {address_info}. "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_exit_sendto(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the return value from the contents
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        ret = data['ret']

        # Assessing the result of the system call
        if int(ret) >= 0:
            result_info = f"successfully sent {ret} bytes"
        else:
            result_info = "failed with an error"

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed a 'sendto' system call. "
            f"The call {result_info}. "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_entry_inotify_add_watch(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the contents into a dictionary for easy access
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        fd = data['fd']
        pathname = data['pathname']
        mask = data['mask']

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} initiated a 'inotify_add_watch' system call. "
            f"This system call attempts to add a watch for the directory or file at '{pathname}' with the file descriptor {fd} and mask {mask}. "
            f"The watch settings correspond to various event notifications. "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_exit_inotify_add_watch(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the contents into a dictionary for easy access
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        ret = data['ret']
        status_description = "successfully" if ret == '0' else f"failed with error code {ret}"

        description = (
            f"At {timestamp}, the 'inotify_add_watch' system call completed {status_description}. "
            f"Process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} attempted to add a file or directory watch, which "
            f"{status_description}. Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_entry_chmod(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the contents into a dictionary for easy access
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        filename = data['filename']
        mode = int(data['mode'], 0)
        mode_str = f'{mode:o}'

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} issued a 'chmod' system call "
            f"to change the permissions of the file '{filename}' to {mode_str} (octal). "
            f"The request was made from the source file located at {source}."
        )
        return description
    def describe_syscall_exit_chmod(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        # Extracting the contents into a dictionary for easy access
        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        ret_code = int(data['ret'])
        status = "successfully" if ret_code == 0 else "unsuccessfully"

        description = (
            f"At {timestamp}, process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} completed the 'chmod' system call "
            f"{status}. The return code was {ret_code}, indicating the operation status. "
            f"The call was issued from the source file located at {source}."
        )
        return description
    def describe_syscall_entry_statfs(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        pathname = data['pathname']

        description = (
            f"At {timestamp}, the 'statfs' system call was initiated. "
            f"Process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} attempted to get file system statistics for {pathname}. "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_exit_statfs(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        ret = data['ret']
        buf = data['buf']
        status_description = "successfully" if ret == '0' else f"failed with error code {ret}"

        description = (
            f"At {timestamp}, the 'statfs' system call completed {status_description}. "
            f"Process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} attempted to get file system statistics, which "
            f"{status_description}. The buffer used for storing the statistics is located at {buf}. "
            f"Source of this system call is located at {source}."
        )
        return description
    def describe_syscall_entry_flock(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        fd = data['fd']
        cmd = data['cmd']

        # Mapping of cmd values to human-readable descriptions
        cmd_map = {
            '1': 'LOCK_SH (shared lock)',
            '2': 'LOCK_EX (exclusive lock)',
            '3': 'LOCK_UN (unlock)',
            '4': 'LOCK_NB (non-blocking lock)'
        }

        cmd_description = cmd_map.get(cmd, f"unknown command ({cmd})")

        description = (
            f"At {timestamp}, the 'flock' system call was invoked by process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id}. "
            f"This call is used to apply or remove an advisory lock on the file descriptor {fd}. "
            f"The command issued was {cmd_description}. The source code location for this system call is {source}."
        )
        return description
    def describe_syscall_exit_flock(self, row):
        timestamp = row['Timestamp']
        cpu_id = row['CPU']
        tid = row['TID']
        prio = row['Prio']
        pid = row['PID']
        source = row['Source']

        contents = row['Contents'].split(', ')
        data = {}
        for item in contents:
            if '=' in item:
                key, value = item.split('=', 1)
                data[key.strip()] = value.strip()

        ret = data['ret']
        status_description = "successfully" if ret == '0' else f"failed with error code {ret}"

        description = (
            f"At {timestamp}, the 'flock' system call completed {status_description}. "
            f"Process {pid} (TID {tid}, priority {prio}) on CPU {cpu_id} attempted to apply or remove an advisory lock, which "
            f"{status_description}. Source of this system call is located at {source}."
        )
        return description

    def process_events(self, event_type):
        event_idx = self.df['Event type'] == event_type
        if event_type == 'power_cpu_idle':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_power_cpu_idle, axis=1)
        elif event_type == 'sched_switch':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_sched_switch, axis=1)
        elif event_type == 'kmem_kmalloc':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_kmem_kmalloc, axis=1)
        elif event_type == 'kmem_kfree':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_kmem_kfree, axis=1)
        elif event_type == 'sched_waking':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_sched_waking, axis=1)
        elif event_type == 'sched_wakeup':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_sched_wakeup, axis=1)
        elif event_type == 'rcu_utilization':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_rcu_utilization, axis=1)
        elif event_type == 'syscall_exit_epoll_wait':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_epoll_wait,axis=1)
        elif event_type == 'kmem_cache_alloc':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_kmem_cache_alloc, axis=1)
        elif event_type == 'syscall_entry_ioctl':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_ioctl, axis=1)
        elif event_type == 'x86_irq_vectors_call_function_entry':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_x86_irq_vectors_call_function_entry, axis=1)
        elif event_type == 'x86_irq_vectors_call_function_exit':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(
                self.describe_x86_irq_vectors_call_function_exit, axis=1)
        elif event_type == 'kmem_cache_free':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_kmem_cache_free, axis=1)
        elif event_type == 'syscall_exit_ioctl':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_ioctl, axis=1)
        elif event_type == 'syscall_entry_splice':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_splice, axis=1)
        elif event_type == 'kmem_mm_page_alloc':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_kmem_mm_page_alloc, axis=1)
        elif event_type == 'writeback_mark_inode_dirty':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_writeback_mark_inode_dirty, axis=1)
        elif event_type == 'writeback_dirty_inode_start':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_writeback_dirty_inode_start, axis=1)
        elif event_type == 'block_touch_buffer':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_block_touch_buffer, axis=1)
        elif event_type == 'writeback_dirty_inode':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_writeback_dirty_inode, axis=1)
        elif event_type == 'block_dirty_buffer':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_block_dirty_buffer, axis=1)
        elif event_type == 'writeback_dirty_page':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_writeback_dirty_page, axis=1)
        elif event_type == 'kmem_mm_page_free':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_kmem_mm_page_free, axis=1)
        elif event_type == 'syscall_entry_sync_file_range':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_sync_file_range, axis=1)
        elif event_type == 'block_bio_remap':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_block_bio_remap, axis=1)
        elif event_type == 'kmem_kmalloc_node':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_kmem_kmalloc_node, axis=1)
        elif event_type == 'syscall_exit_sync_file_range':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_sync_file_range, axis=1)
        elif event_type == 'sched_stat_runtime':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_sched_stat_runtime, axis=1)
        elif event_type == 'power_cpu_frequency':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_power_cpu_frequency, axis=1)
        elif event_type == 'sched_process_free':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_sched_process_free, axis=1)
        elif event_type == 'syscall_entry_sendmsg':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_sendmsg, axis=1)
        elif event_type == 'syscall_exit_sendmsg':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_sendmsg, axis=1)
        elif event_type == 'syscall_entry_close':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_close, axis=1)
        elif event_type == 'syscall_exit_close':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_close, axis=1)
        elif event_type == 'syscall_entry_epoll_wait':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_epoll_wait, axis=1)
        elif event_type == 'sched_migrate_task':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_sched_migrate_task, axis=1)
        elif event_type == 'syscall_exit_recvmsg':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_recvmsg, axis=1)
        elif event_type == 'syscall_entry_shutdown':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_shutdown, axis=1)
        elif event_type == 'syscall_exit_shutdown':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_shutdown, axis=1)
        elif event_type == 'syscall_entry_newfstat':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_newfstat, axis=1)
        elif event_type == 'syscall_exit_newfstat':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_newfstat, axis=1)
        elif event_type == 'syscall_entry_mmap':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_mmap, axis=1)
        elif event_type == 'syscall_exit_mmap':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_mmap, axis=1)
        elif event_type == 'syscall_entry_write':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_write, axis=1)
        elif event_type == 'syscall_exit_write':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_write, axis=1)
        elif event_type == 'syscall_entry_exit_group':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_exit_group, axis=1)
        elif event_type == 'sched_process_exit':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_sched_process_exit, axis=1)
        elif event_type == 'syscall_exit_wait4':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_wait4, axis=1)
        elif event_type == 'syscall_entry_rt_sigaction':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_rt_sigaction, axis=1)
        elif event_type == 'syscall_exit_rt_sigaction':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_rt_sigaction, axis=1)
        elif event_type == 'syscall_entry_rt_sigprocmask':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_rt_sigprocmask, axis=1)
        elif event_type == 'syscall_exit_rt_sigprocmask':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_rt_sigprocmask, axis=1)
        elif event_type == 'syscall_entry_wait4':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_wait4, axis=1)
        elif event_type == 'sched_process_wait':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_sched_process_wait, axis=1)
        elif event_type == 'syscall_entry_unknown':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_unknown, axis=1)
        elif event_type == 'syscall_entry_read':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_read, axis=1)
        elif event_type == 'syscall_exit_read':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_read, axis=1)
        elif event_type == 'syscall_entry_lseek':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_lseek, axis=1)
        elif event_type == 'syscall_exit_lseek':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_lseek, axis=1)
        elif event_type == 'syscall_entry_clone':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_clone, axis=1)
        elif event_type == 'sched_process_fork':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_sched_process_fork, axis=1)
        elif event_type == 'sched_wakeup_new':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_sched_wakeup_new, axis=1)
        elif event_type == 'syscall_exit_clone':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_clone, axis=1)
        elif event_type == 'syscall_entry_execve':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_execve, axis=1)
        elif event_type == 'sched_process_exec':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_sched_process_exec, axis=1)
        elif event_type == 'syscall_exit_execve':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_execve, axis=1)
        elif event_type == 'syscall_entry_brk':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_brk, axis=1)
        elif event_type == 'syscall_exit_brk':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_brk, axis=1)
        elif event_type == 'syscall_entry_access':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_access, axis=1)
        elif event_type == 'syscall_exit_access':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_access, axis=1)
        elif event_type == 'syscall_entry_open':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_open, axis=1)
        elif event_type == 'syscall_exit_open':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_open, axis=1)
        elif event_type == 'syscall_entry_mprotect':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_mprotect, axis=1)
        elif event_type == 'syscall_exit_mprotect':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_mprotect, axis=1)
        elif event_type == 'syscall_exit_unknown':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_unknown, axis=1)
        elif event_type == 'syscall_entry_munmap':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_munmap, axis=1)
        elif event_type == 'syscall_exit_munmap':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_munmap, axis=1)
        elif event_type == 'syscall_entry_getpid':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_getpid, axis=1)
        elif event_type == 'syscall_exit_getpid':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_getpid, axis=1)
        elif event_type == 'syscall_entry_geteuid':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_geteuid, axis=1)
        elif event_type == 'syscall_exit_geteuid':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_geteuid, axis=1)
        elif event_type == 'syscall_entry_getppid':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_getppid, axis=1)
        elif event_type == 'syscall_exit_getppid':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_getppid, axis=1)
        elif event_type == 'syscall_entry_newstat':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_newstat, axis=1)
        elif event_type == 'syscall_exit_newstat':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_newstat, axis=1)
        elif event_type == 'syscall_entry_fcntl':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_fcntl, axis=1)
        elif event_type == 'syscall_exit_fcntl':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_fcntl, axis=1)
        elif event_type == 'syscall_entry_pipe':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_pipe, axis=1)
        elif event_type == 'syscall_exit_pipe':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_pipe, axis=1)
        elif event_type == 'syscall_entry_dup2':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_dup2, axis=1)
        elif event_type == 'syscall_exit_dup2':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_dup2, axis=1)
        elif event_type == 'syscall_entry_chdir':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_chdir, axis=1)
        elif event_type == 'syscall_exit_chdir':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_chdir, axis=1)
        elif event_type == 'syscall_entry_getdents':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_getdents, axis=1)
        elif event_type == 'syscall_exit_getdents':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_getdents, axis=1)
        elif event_type == 'syscall_entry_faccessat':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_faccessat, axis=1)
        elif event_type == 'syscall_exit_faccessat':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_faccessat, axis=1)
        elif event_type == 'syscall_entry_getuid':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_getuid, axis=1)
        elif event_type == 'syscall_exit_getuid':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_getuid, axis=1)
        elif event_type == 'syscall_entry_getgid':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_getgid, axis=1)
        elif event_type == 'syscall_exit_getgid':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_getgid, axis=1)
        elif event_type == 'syscall_entry_mkdir':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_mkdir, axis=1)
        elif event_type == 'syscall_exit_mkdir':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_mkdir, axis=1)
        elif event_type == 'syscall_entry_set_tid_address':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_set_tid_address, axis=1)
        elif event_type == 'syscall_exit_set_tid_address':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_set_tid_address, axis=1)
        elif event_type == 'syscall_entry_set_robust_list':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_set_robust_list, axis=1)
        elif event_type == 'syscall_exit_set_robust_list':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_set_robust_list, axis=1)
        elif event_type == 'syscall_entry_getrlimit':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_getrlimit, axis=1)
        elif event_type == 'syscall_exit_getrlimit':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_getrlimit, axis=1)
        elif event_type == 'syscall_entry_getcwd':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_getcwd, axis=1)
        elif event_type == 'syscall_exit_getcwd':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_getcwd, axis=1)
        elif event_type == 'syscall_entry_newlstat':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_newlstat, axis=1)
        elif event_type == 'syscall_exit_newlstat':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_newlstat, axis=1)
        elif event_type == 'syscall_entry_futex':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_futex, axis=1)
        elif event_type == 'syscall_exit_futex':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_futex, axis=1)
        elif event_type == 'syscall_entry_pipe2':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_pipe2, axis=1)
        elif event_type == 'syscall_exit_pipe2':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_pipe2, axis=1)
        elif event_type == 'syscall_entry_socket':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_socket, axis=1)
        elif event_type == 'syscall_exit_socket':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_socket, axis=1)
        elif event_type == 'syscall_entry_connect':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_connect, axis=1)
        elif event_type == 'syscall_exit_connect':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_connect, axis=1)
        elif event_type == 'syscall_entry_newuname':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_newuname, axis=1)
        elif event_type == 'syscall_exit_newuname':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_newuname, axis=1)
        elif event_type == 'syscall_entry_poll':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_poll, axis=1)
        elif event_type == 'syscall_exit_poll':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_poll, axis=1)
        elif event_type == 'syscall_entry_sendmmsg':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_sendmmsg, axis=1)
        elif event_type == 'syscall_exit_sendmmsg':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_sendmmsg, axis=1)
        elif event_type == 'syscall_entry_recvfrom':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_recvfrom, axis=1)
        elif event_type == 'syscall_exit_recvfrom':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_recvfrom, axis=1)
        elif event_type == 'syscall_entry_fadvise64':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_fadvise64, axis=1)
        elif event_type == 'syscall_exit_fadvise64':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_fadvise64, axis=1)
        elif event_type == 'syscall_entry_getsockopt':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_getsockopt, axis=1)
        elif event_type == 'syscall_exit_getsockopt':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_getsockopt, axis=1)
        elif event_type == 'syscall_entry_sendto':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_sendto, axis=1)
        elif event_type == 'syscall_exit_sendto':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_sendto, axis=1)
        elif event_type == 'syscall_entry_inotify_add_watch':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_inotify_add_watch, axis=1)
        elif event_type == 'syscall_exit_inotify_add_watch':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_inotify_add_watch, axis=1)
        elif event_type == 'syscall_entry_chmod':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_chmod, axis=1)
        elif event_type == 'syscall_exit_chmod':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_chmod, axis=1)
        elif event_type == 'syscall_entry_statfs':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_statfs, axis=1)
        elif event_type == 'syscall_exit_statfs':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_statfs, axis=1)
        elif event_type == 'syscall_entry_flock':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_entry_flock, axis=1)
        elif event_type == 'syscall_exit_flock':
            self.df.loc[event_idx, 'Description'] = self.df.loc[event_idx].apply(self.describe_syscall_exit_flock, axis=1)
        return self.df.loc[event_idx, 'Description'].tolist()
