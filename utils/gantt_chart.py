import matplotlib.pyplot as plt
import random

def draw_gantt_chart(gantt):
    fig, ax = plt.subplots(figsize=(10, 3))
    y_pos = 1
    
    #generating random distinct colors for each process 
    process_colors = {}
    for task in gantt:
        pid = task[0]
        if pid not in process_colors:
            #assinging a random color to each process
            process_colors[pid] = (random.random(), random.random(), random.random())

    for task in gantt:
        pid, start, end = task
        ax.broken_barh([(start, end - start)], (y_pos, 1), facecolors=(process_colors[pid]))
        ax.text((start + end) / 2, y_pos + 0.5, pid, ha='center', va='center', color='white', fontsize=10, weight='bold')

    #customizing the chart appearance
    ax.set_yticks([])
    ax.set_xticks(range(0, gantt[-1][2] + 1, 1))
    ax.set_xlim(0, gantt[-1][2])
    plt.xlabel("Time")
    plt.title("Gantt Chart")
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()
