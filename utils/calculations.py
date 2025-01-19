def calculate_tat_wt(processes):
    for p in processes:
        p['turnaround_time'] = p['finish_time'] - p['arrival_time']
        p['waiting_time'] = p['turnaround_time'] - p['burst_time']
