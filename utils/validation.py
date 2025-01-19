def validate_input(prompt, expected_type, condition):
    while True:
        try:
            value = expected_type(input(prompt))
            if not condition(value):
                raise ValueError("Input does not meet required condition.")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")


def validate_gantt_chart(gantt, processes):
    print("\nValidating Gantt Chart...")
    #mapping process IDs to their burst times
    process_burst_times = {p['pid']: p['burst_time'] for p in processes}
    process_burst_counts = {p['pid']: 0 for p in processes}
    total_time = 0

    for segment in gantt:
        pid, start, end = segment
        execution_time = end - start
        total_time += execution_time

        #checking if the process exists
        if pid not in process_burst_times:
            raise ValueError(f"Error: Process '{pid}' in Gantt chart does not exist.")

        #countig executed burst times
        process_burst_counts[pid] += execution_time

        #check if execution time is valid
        if execution_time <= 0:
            raise ValueError(f"Error: Invalid execution time for process '{pid}'.")

    #lastly check if total burst time matches
    for pid, burst_time in process_burst_times.items():
        if process_burst_counts[pid] != burst_time:
            raise ValueError(f"Error: Gantt chart does not correctly represent process '{pid}' (Expected: {burst_time}, Got: {process_burst_counts[pid]}).")

    print("Gantt Chart Validation Passed!\n")
