from utils.calculations import calculate_tat_wt

def round_robin(processes, time_quantum):
    processes = sorted(processes, key=lambda p: p['arrival_time'])  #sort by arrival time (FCFS for ties)
    time = 0
    queue = []
    gantt = []
    remaining_burst = {p['pid']: p['burst_time'] for p in processes}

    while remaining_burst:
        #add processes that have arrived to the queue
        for p in processes:
            if (
                p['arrival_time'] <= time 
                and p['pid'] not in queue 
                and p['pid'] in remaining_burst
            ):
                queue.append(p['pid'])

        #if no process is ready, skip time
        if not queue:
            time += 1
            continue

        #dequeue the next process
        current = queue.pop(0)
        execute_time = min(time_quantum, remaining_burst[current])  #execute for time quantum or remaining burst time
        gantt.append((current, time, time + execute_time))
        time += execute_time
        remaining_burst[current] -= execute_time

        #add processes that arrived during this execution (from ready q)
        for p in processes:
            if (
                p['arrival_time'] > gantt[-1][1] 
                and p['arrival_time'] <= gantt[-1][2] 
                and p['pid'] not in queue 
                and p['pid'] in remaining_burst
            ):
                queue.append(p['pid'])

        #if the process still has burst time remaining, requeue it
        if remaining_burst[current] > 0:
            queue.append(current)
        else:
            #mark process as finished
            for p in processes:
                if p['pid'] == current:
                    p['finish_time'] = time
            del remaining_burst[current]  #remove/delete process from remaining burst

    #calculating TAT and WT
    calculate_tat_wt(processes)
    avg_tat = sum(p['turnaround_time'] for p in processes) / len(processes)
    avg_wt = sum(p['waiting_time'] for p in processes) / len(processes)

    return {
        "gantt": gantt,
        "processes": processes,
        "avg_tat": avg_tat,
        "avg_wt": avg_wt,
    }
