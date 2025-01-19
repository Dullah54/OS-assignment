from utils.calculations import calculate_tat_wt

def preemptive_priority(processes):
    processes = sorted(processes, key=lambda p: p['arrival_time'])  # Sort by arrival time
    time = 0
    gantt = []
    remaining_burst = {p['pid']: p['burst_time'] for p in processes}
    current_process = None

    while remaining_burst:
        #identify all the ready processes
        ready = [
            p for p in processes if p['arrival_time'] <= time and p['pid'] in remaining_burst
        ]
        if not ready:
            time += 1
            continue

        #check if we need to preempt the current process
        if current_process and current_process['pid'] in remaining_burst:
            #if new process has the same priority or burst time as the current process,we avoid preemption
            higher_priority = [
                p for p in ready if p['priority'] < current_process['priority']
            ]
            if not higher_priority:
                #accumulate contiguous execution in gantt chart
                if gantt and gantt[-1][0] == current_process['pid']:
                    gantt[-1] = (current_process['pid'], gantt[-1][1], time + 1)
                else:
                    gantt.append((current_process['pid'], time, time + 1))
                time += 1
                remaining_burst[current_process['pid']] -= 1

                #if the current process finishes, we record its finish time and remove it
                if remaining_burst[current_process['pid']] == 0:
                    for p in processes:
                        if p['pid'] == current_process['pid']:
                            p['finish_time'] = time
                    del remaining_burst[current_process['pid']]
                continue

        #select the process with the highest priority (lower value = higher priority)
        current_process = min(ready, key=lambda p: p['priority'])

        #accumulate contiguous execution in the gantt chart again
        if gantt and gantt[-1][0] == current_process['pid']:
            gantt[-1] = (current_process['pid'], gantt[-1][1], time + 1)
        else:
            gantt.append((current_process['pid'], time, time + 1))

        time += 1
        remaining_burst[current_process['pid']] -= 1

        #if the current process finishes,we again record its finish time and remove it
        if remaining_burst[current_process['pid']] == 0:
            for p in processes:
                if p['pid'] == current_process['pid']:
                    p['finish_time'] = time
            del remaining_burst[current_process['pid']]

    #calculating turnaround time (TAT) and waiting time (WT)
    calculate_tat_wt(processes)
    avg_tat = sum(p['turnaround_time'] for p in processes) / len(processes)
    avg_wt = sum(p['waiting_time'] for p in processes) / len(processes)
    
    return {"gantt": gantt, "processes": processes, "avg_tat": avg_tat, "avg_wt": avg_wt}
