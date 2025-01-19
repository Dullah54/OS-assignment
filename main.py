from algorithms.round_robin import round_robin
from algorithms.srt import srt
from algorithms.sjn import sjn
from algorithms.preemptive_priority import preemptive_priority
from utils.gantt_chart import draw_gantt_chart
from utils.validation import validate_input
import pandas as pd

def main():
    print("\n=== CPU Scheduling Simulator ===")
    print("Part A: Round Robin (Compulsory)\n")

    # Part A: Round Robin(RR)
    num_processes = validate_input("Enter the number of processes (3-10): ", int, lambda x: 3 <= x <= 10)
    processes = []
    for i in range(num_processes):
        pid = f"P{i}"
        print(f"\nProcess {pid}:")
        arrival_time = validate_input("  Arrival Time: ", int, lambda x: x >= 0)
        burst_time = validate_input("  Burst Time: ", int, lambda x: x > 0)
        priority = validate_input("  Priority (lower = higher priority): ", int, lambda x: x > 0)
        processes.append({
            "pid": pid,
            "arrival_time": arrival_time,
            "burst_time": burst_time,
            "priority": priority,
        })

    rr_result = round_robin(processes, time_quantum=3)
    print("\nGantt Chart (Round Robin):")
    draw_gantt_chart(rr_result['gantt'])
    print("\nProcess Statistics (Round Robin):")
    print("+-----------+------------------+-----------------------+------------------------+----------------+--------------------+")
    print("| Processes | Finish Time (FT) | Arrival Time (AT)     | Turnaround Time (TAT)  | Burst Time (BT)| Waiting Time (WT)  |")
    print("+-----------+------------------+-----------------------+------------------------+----------------+--------------------+")
    for p in rr_result['processes']:
        print("| {:<9} | {:<16} | {:<21} | {:<22} | {:<14} | {:<18} |".format(
            p['pid'], p['finish_time'], p['arrival_time'], p['turnaround_time'], p['burst_time'], p['waiting_time']
        ))
    print("+-----------+------------------+-----------------------+------------------------+----------------+--------------------+")
    print(f"Average TAT: {rr_result['avg_tat']:.2f}, Average WT: {rr_result['avg_wt']:.2f}")

    #option to exit after Part A
    should_exit = validate_input("\nDo you want to exit? (yes/no): ", str, lambda x: x.lower() in ["yes", "no"])
    if should_exit.lower() == "yes":
        print("Exiting the simulator. Goodbye!")
        return

    # Part B: Loop through options until the user chooses to exit
    while True:
        print("\nPart B: Choose Scheduling Algorithm")
        print("1. Shortest Remaining Time (SRT)")
        print("2. Shortest Job Next (SJN)")
        print("3. Preemptive Priority")
        print("4. Exit")
        choice = validate_input("Choose an option (1-4): ", int, lambda x: x in [1, 2, 3, 4])

        if choice == 4:
            print("Exiting the simulator. Goodbye!")
            break

        if choice == 1:
            result = srt(processes)
            algorithm = "Shortest Remaining Time (SRT)"
        elif choice == 2:
            result = sjn(processes)
            algorithm = "Shortest Job Next (SJN)"
        elif choice == 3:
            result = preemptive_priority(processes)
            algorithm = "Preemptive Priority"

        print(f"\nGantt Chart ({algorithm}):")
        draw_gantt_chart(result['gantt'])
        print(f"\nProcess Statistics ({algorithm}):")
        print("+-----------+------------------+-----------------------+------------------------+----------------+--------------------+")
        print("| Processes | Finish Time (FT) | Arrival Time (AT)     | Turnaround Time (TAT)  | Burst Time (BT)| Waiting Time (WT)  |")
        print("+-----------+------------------+-----------------------+------------------------+----------------+--------------------+")
        for p in result['processes']:
            print("| {:<9} | {:<16} | {:<21} | {:<22} | {:<14} | {:<18} |".format(
                p['pid'], p['finish_time'], p['arrival_time'], p['turnaround_time'], p['burst_time'], p['waiting_time']
            ))
        print("+-----------+------------------+-----------------------+------------------------+----------------+--------------------+")
        print(f"Average TAT: {result['avg_tat']:.2f}, Average WT: {result['avg_wt']:.2f}")

if __name__ == "__main__":
    main()
