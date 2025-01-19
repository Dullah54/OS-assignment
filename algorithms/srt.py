from utils.calculations import calculate_tat_wt

def srt(processes):
    processes = sorted(processes, key=lambda p: p['arrival_time'])  #sorting by AT
    time = 0
    gantt = []
    remaining_burst = {p['pid']: p['burst_time'] for p in processes}

    while remaining_burst:
        ready = [
            p for p in processes if p['arrival_time'] <= time and p['pid'] in remaining_burst
        ]
        if not ready:
            time += 1
            continue

        #select the process with the shortest remaining time, tie breaker FCFS
        current_process = min(ready, key=lambda p: (remaining_burst[p['pid']], p['arrival_time']))

        #accumulate contiguous execution in gantt chart
        if gantt and gantt[-1][0] == current_process['pid']:
            gantt[-1] = (current_process['pid'], gantt[-1][1], time + 1)
        else:
            gantt.append((current_process['pid'], time, time + 1))

        time += 1
        remaining_burst[current_process['pid']] -= 1

        if remaining_burst[current_process['pid']] == 0:
            for p in processes:
                if p['pid'] == current_process['pid']:
                    p['finish_time'] = time
            del remaining_burst[current_process['pid']]       

    calculate_tat_wt(processes)
    avg_tat = sum(p['turnaround_time'] for p in processes) / len(processes)
    avg_wt = sum(p['waiting_time'] for p in processes) / len(processes)
    return {"gantt": gantt, "processes": processes, "avg_tat": avg_tat, "avg_wt": avg_wt}
