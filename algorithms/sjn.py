from utils.calculations import calculate_tat_wt

def sjn(processes):
    processes = sorted(processes, key=lambda p: p['arrival_time'])  #sorting by the arrival time of each process
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

        #select process with the shortest burst time, tie breaker FCFD
        current_process = min(ready, key=lambda p: (p['burst_time'], p['arrival_time']))
        gantt.append((current_process['pid'], time, time + remaining_burst[current_process['pid']]))
        time += remaining_burst[current_process['pid']]
        del remaining_burst[current_process['pid']]

        for p in processes:
            if p['pid'] == current_process['pid']:
                p['finish_time'] = time

    calculate_tat_wt(processes)
    avg_tat = sum(p['turnaround_time'] for p in processes) / len(processes)
    avg_wt = sum(p['waiting_time'] for p in processes) / len(processes)
    return {"gantt": gantt, "processes": processes, "avg_tat": avg_tat, "avg_wt": avg_wt}
