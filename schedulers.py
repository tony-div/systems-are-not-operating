class Schedulers:
  # def __init__(self, value):
  #   self.value = value

  def simulate(algo_name: str, processes_list, time_quanta=0):
    # [arrival time, burst_time, process_id]
    match algo_name:
        case "SJF_non_preemptive":
            return Schedulers.SJF_non_preemptive(processes_list)
        case "preemptive_sjf" :
            return Schedulers.preemptive_sjf(processes_list)
        case "fcfs":
            return Schedulers.fcfs(processes_list)
        case "round_robin":
            return Schedulers.round_robin(processes_list, time_quanta)
        case "Priority_Non_Preemptive":
            return Schedulers.priority(processes_list)
        case "priority_preemptive" :
            return Schedulers.priority_preemptive(processes_list)
        case _:
            return "invalid input"
  
  def SJF_non_preemptive(process_list):
    # [arrival time, burst time, process id]
    t = 0
    Gantt = []
    completed = {}
    CT = []
    TT = []
    WT = []

    while process_list:
        available = []
        for p in process_list:
            if p[0] <= t:  # Arrival time is now the first parameter
                available.append(p)

        if available == []:
            t += 1
            Gantt.append('idle')

        else:            
            available.sort(key=lambda x: (x[1], x[0]))  # Sort by burst time, then by arrival time
            process = available[0]
            PID = process[2]
            arrival_time = process[0]
            burst_time = process[1]

            Gantt.append({"name": str(PID), "interval": [t, t+burst_time]})
            t += burst_time

            ct = t  # Completion time
            CT.append(ct)
            tt = ct - arrival_time  # Turnaround time
            TT.append(tt)
            wt = tt - burst_time  # Waiting time
            WT.append(wt)
            completed[PID] = [ct, tt, wt]

            process_list.remove(process)

    # print("\nGantt Chart:")
    # print(" -> ".join(Gantt))
    pid_arr=[]
    ct_arr=[]
    tat_arr=[]
    wt_arr=[]

    # print("\nProcess\tCT\tTAT\tWT")
    for pid in completed:
        ct, tat, wt = completed[pid]
        # print(f"{pid}\t{ct}\t{tat}\t{wt}")
        pid_arr.append(pid)
        ct_arr.append(ct)
        tat_arr.append(tat)
        wt_arr.append(wt)

    # print('\nAverage Completion time =', sum(CT) / len(CT))
    # print('Average Turnaround time =', sum(TT) / len(TT))
    # print('Average Waiting time =', sum(WT) / len(WT))
  # print("************************")
    #print (completed)
    #print(Gantt)
    return {"chart": Gantt,
            "processes" :pid_arr,
            "turnaround_time" : tat_arr ,
            "waiting_time" : wt_arr,
            "response_time": wt_arr,
            "avg_turnaround_time":sum(TT) / len(TT) ,
            "avg_waiting_time": sum(WT) / len(WT),
            "avg_response_time": sum(WT) / len(WT)
            }
  
  def preemptive_sjf(process_list):
    t = 0
    completed = {}
    gantt = []
    ready_queue = []

    # Sort processes by arrival time
    process_list.sort()

    # Clone burst times for tracking remaining burst times
    remaining_burst = {p[2]: p[1] for p in process_list}
    first_response = {}  # To track the response time of each process

    while process_list or ready_queue:
        # Add processes that have arrived to the ready queue
        while process_list and process_list[0][0] <= t:
            ready_queue.append(process_list.pop(0))

        # If ready queue is empty, CPU is idle
        if not ready_queue:
            gantt.append("Idle")
            t += 1
            continue

        # Select the process with the shortest remaining burst time
        ready_queue.sort(key=lambda x: remaining_burst[x[2]])
        current_process = ready_queue[0]

        # Log response time if the process starts execution for the first time
        if current_process[2] not in first_response:
            first_response[current_process[2]] = t - current_process[0]

        if len(gantt) > 0 and gantt[-1]["name"] == str(current_process[2]):
          gantt[-1]["interval"][1] = t+1
        else:
          gantt.append({"name": str(current_process[2]), "interval":[t, t+1]})
        # Execute the process for 1 unit of time
        remaining_burst[current_process[2]] -= 1
        t += 1

        # If the process is completed
        if remaining_burst[current_process[2]] == 0:
            ready_queue.pop(0)
            ct = t  # Completion time
            at = current_process[0]  # Arrival time
            bt = current_process[1]  # Original burst time
            tt = ct - at  # Turnaround Time
            wt = tt - bt  # Waiting Time
            rt = first_response[current_process[2]]  # Response Time
            completed[current_process[2]] = [ct, tt, wt, rt]

    # Calculate and display results
    # print("\nGantt Chart:")
    # print(" -> ".join(gantt))

    PID_arr=[]
    CT_arr=[]
    TT_arr=[]
    WT_arr=[]
    RT_arr=[]

    # print("\nProcess Details:")
    # print("Process\tCT\tTAT\tWT\tRT")
    total_tt = total_wt = total_rt = 0
    for process_id, values in completed.items():
        ct, tt, wt, rt = values
        total_tt += tt
        total_wt += wt
        total_rt += rt
        # print(f"{process_id}\t{ct}\t{tt}\t{wt}\t{rt}")
        PID_arr.append(process_id)
        CT_arr.append(ct)
        TT_arr.append(tt)
        WT_arr.append(wt)
        RT_arr.append(rt)

    # Display averages
    n = len(completed)
    # print("\nAverages:")
    # print(f"Average Turnaround Time: {total_tt / n:.2f}")
    # print(f"Average Waiting Time: {total_wt / n:.2f}")
    # print(f"Average Response Time: {total_rt / n:.2f}")
    return{"chart":gantt,
          "processes":PID_arr,
          "turnaround_time":TT_arr,
          "waiting_time":WT_arr,
          "response_time":RT_arr,
          "avg_turnaround_time":total_tt / n ,
          "avg_waiting_time": total_wt / n,
          "avg_response_time": total_rt / n}

  def fcfs(process_list):
    # Initialize the current time, Gantt chart, and dictionaries for completed processes
    t = 0  # Current time
    gantt = []  # Gantt chart to track the execution sequence
    completed = {}  # Dictionary to store completion details of each process (CT, TAT, WT)
    detailed_process = []  # List to store detailed process info (PID, AT, BT, ST, CT, TAT, WT, RT)

    # Process the processes in the sorted list
    for i in range(len(process_list)):
        # Check if arrival time (AT) is provided, otherwise set it to zero
        if len(process_list[i]) == 2:  # If only BT and PID are provided
            process_list[i].insert(0, 0)  # Set arrival time to 0
    def sort_by_AT(process):
      return process[0]
    # print(process_list)
    process_list.sort(key=sort_by_AT)  # Sort the processes by arrival time (AT)
    # print(process_list)
    while process_list:
        # If the first process has not arrived yet (AT > current time t), the system is idle
        if process_list[0][0] > t:
            t += 1  # Increment time to simulate idle period
            gantt.append("Idle")  # Mark idle time in the Gantt chart
            continue  # Skip the rest of the loop and check again
        else:
            # Pop the first process from the list for execution
            process = process_list.pop(0)
            at, bt, pid = process  # Unpack the process details (AT, BT, PID)

            # Start time is the maximum of current time t or arrival time AT
            st = max(t, at)  # Start time (ST)
            t = st + bt      # Update current time to the completion of this process
            ct = t           # Completion time (CT)
            tat = ct - at    # Turnaround time (TAT) = CT - AT
            wt = tat - bt    # Waiting time (WT) = TAT - BT
            rt = st - at     # Response time (RT) = ST - AT

            # Store the completion details in the dictionary
            completed[pid] = [ct, tat, wt]
            # Append detailed information for each process
            detailed_process.append([pid, at, bt, st, ct, tat, wt, rt])
            # Extend the Gantt chart by adding the process's ID for the burst time duration
            gantt.append({"name": str(pid), "interval": [st, t]})

    # Display Gantt Chart (shows the execution order of processes and idle times)
    # print("Gantt Chart:", gantt)

    # Display the detailed process table showing key metrics for each process
    # print("\nProcess Details:")
    # print("Process\tAT\tBT\tST\tCT\tTAT\tWT\tRT")
    process_arr=[]
    AT_arr=[]
    BT_arr=[]
    ST_arr=[]
    CT_arr=[]
    TAT_arr=[]
    WT_arr=[]
    RT_arr=[]
    for process in detailed_process:
        # print("\t".join(map(str, process)))  # Print each process' details in a table format
        process_arr.append(process[0])
        AT_arr.append(process[1])
        BT_arr.append(process[2])
        ST_arr.append(process[3])
        CT_arr.append(process[4])
        TAT_arr.append(process[5])
        WT_arr.append(process[6])
        RT_arr.append(process[7])

    # Calculate and display the averages for Turnaround Time (TAT), Waiting Time (WT), and Response Time (RT)
    avg_tat = sum(p[5] for p in detailed_process) / len(detailed_process)  # Average TAT
    avg_wt = sum(p[6] for p in detailed_process) / len(detailed_process)  # Average WT
    avg_rt = sum(p[7] for p in detailed_process) / len(detailed_process)  # Average RT

    # Output the average times for each metric
    # print("\nAverages for FCFS algorithm:")
    # print("Average Turnaround Time:", round(avg_tat, 2))
    # print("Average Waiting Time:", round(avg_wt, 2))
    # print("Average Response Time:", round(avg_rt, 2))
    return {"chart" :gantt,
            "processes":process_arr,
            "turnaround_time":TAT_arr,
            "waiting_time":WT_arr,
            "response_time":RT_arr,
            "avg_turnaround_time":avg_tat,
            "avg_waiting_time":avg_wt,
            "avg_response_time":avg_rt
            }
  
  def round_robin(process_list, time_quanta):
    t = 0
    gantt = []
    completed = {}
    first_response = {}  # To track the response time

    # Sort processes by arrival time
    def sort_by_AT(process):
      return process[0]
    process_list.sort(key=sort_by_AT) 
    burst_times = {}
    for p in process_list:
        process_id = p[2]
        burst_time = p[1]
        burst_times[process_id] = burst_time

    while process_list:
        available = [p for p in process_list if p[0] <= t]

        # Boundary condition: If no process is available, CPU is idle
        if not available:
            gantt.append("Idle")
            t += 1
            continue

        # Service the first available process
        process = available[0]
        process_list.remove(process)

        # Log the response time for the first execution
        if process[2] not in first_response:
            first_response[process[2]] = t - process[0]
        remaining_burst = process[1]

        if remaining_burst <= time_quanta:
            gantt.append({"name": str(process[2]), "interval": [t, t+remaining_burst]})
            t += remaining_burst
            ct = t  # Completion time
            process_id = process[2]
            arrival_time = process[0]
            burst_time = burst_times[process_id]
            tt = ct - arrival_time  # Turnaround Time
            wt = tt - burst_time   # Waiting Time
            rt = first_response[process_id]  # Response Time
            completed[process[2]] = [ct, tt, wt, rt]
        else:
            gantt.append({"name": str(process[2]), "interval": [t, t+time_quanta]})
            t += time_quanta
            process[1] -= time_quanta
            process_list.append(process)

    # # Calculate and display results
    # print("\nGantt Chart:")
    # print(" -> ".join(gantt))
    PID_arr=[]
    CT_arr=[]
    TT_arr=[]
    WT_arr=[]
    RT_arr=[]

    # print("\nProcess Details:")
    # print("Process\tCT\tTAT\tWT\tRT")
    total_tt = total_wt = total_rt = 0
    for process_id, values in completed.items():
        ct, tt, wt, rt = values
        total_tt += tt
        total_wt += wt
        total_rt += rt
        # print(f"{process_id}\t{ct}\t{tt}\t{wt}\t{rt}")
        PID_arr.append(process_id)
        CT_arr.append(ct)
        TT_arr.append(tt)
        WT_arr.append(wt)
        RT_arr.append(rt)


    # Display averages
    n = len(completed)
    # print("\nAverages:")
    # print(f"Average Turnaround Time: {total_tt / n:.2f}")
    # print(f"Average Waiting Time: {total_wt / n:.2f}")
    # print(f"Average Response Time: {total_rt / n:.2f}")
    # print("******************")
    return{"chart":gantt,
          "processes":PID_arr,
          "turnaround_time":TT_arr,
          "waiting_time":WT_arr,
          "response_time":RT_arr,
          "avg_turnaround_time":total_tt / n ,
          "avg_waiting_time": total_wt / n,
          "avg_response_time": total_rt / n,
          "context_switches": len(gantt) - 1}
  
  def priority(process_list):
    # [AT, BT, PID, Priority]
        # If no arrival time is provided, set all arrival times to 0
    for process in process_list:
        if len(process) == 3:
            process.insert(0, 0)

    gantt = []  # To store the Gantt chart representation of process execution
    t = 0  # Current time
    completed = {}  # Dictionary to store completion details of each process
    response_times = {}  # Dictionary to store response times of processes

    while process_list:
        available = []  # List to store processes that have arrived
        for p in process_list:
            AT = p[0]
            if AT <= t:
                available.append(p)  # Add process to available list if it has arrived

        if not available:
            # If no processes are available, the CPU is idle
            gantt.append("Idle")
            t += 1  # Increment time
            continue
        else:
            # Sort available processes by priority (last element of the list), then by arrival time
            available.sort(key=lambda x: (x[3], x[0]))
            process = available[0]  # Select the process with the highest priority
            process_list.remove(process)  # Remove the selected process from the list

            AT = process[0]  # Arrival time
            BT = process[1]  # Burst time
            pid = process[2]  # Process ID
            priority_value = process[3]  # Priority of the process

            if pid not in response_times:
                # Calculate response time if the process starts for the first time
                response_times[pid] = t - AT

            gantt.append({"name": str(pid), "interval": [t, t+BT]})  # Add the process ID to the Gantt chart
            t += BT  # Update the current time after executing the process

            # Calculate Completion Time (CT), Turnaround Time (TAT), and Waiting Time (WT)
            CT = t  # Completion Time
            TAT = CT - AT  # Turnaround Time = Completion Time - Arrival Time
            WT = TAT - BT  # Waiting Time = Turnaround Time - Burst Time

            # Store the calculated details in the completed dictionary
            completed[pid] = [priority_value, AT, BT, CT, TAT, WT]

    # Print Gantt Chart
    print("Gantt Chart:", gantt)
    PID_arr=[]
    PRI_arr=[]
    AT_arr=[]
    BT_arr=[]
    CT_arr=[]
    TAT_arr=[]
    WT_arr=[]
    RT_arr=[]

    # Print Process Details
    # print("\nPriority Non-Preemptive Process Details:")
    # print("Process\tPri\tAT\tBT\tCT\tTAT\tWT\tRT")

    total_tat = 0  # Total Turnaround Time
    total_wt = 0  # Total Waiting Time
    total_rt = 0  # Total Response Time
    n = len(completed)  # Number of processes

    for pid, details in completed.items():
        priority_value, arrival_time, burst_time, ct, tat, wt = details
        rt = response_times[pid]  # Retrieve response time for the process
        total_tat += tat  # Accumulate Turnaround Time
        total_wt += wt  # Accumulate Waiting Time
        total_rt += rt  # Accumulate Response Time
        # print(f"{pid}\t{priority_value}\t{arrival_time}\t{burst_time}\t{ct}\t{tat}\t{wt}\t{rt}")
        PID_arr.append(pid)
        PRI_arr.append(priority_value)
        AT_arr.append(arrival_time)
        BT_arr.append(burst_time)
        CT_arr.append(ct)
        TAT_arr.append(tat)
        WT_arr.append(wt)
        RT_arr.append(rt)


    # Calculate Averages
    avg_tat = total_tat / n  # Average Turnaround Time
    avg_wt = total_wt / n  # Average Waiting Time
    avg_rt = total_rt / n  # Average Response Time

    print("\nAverages for Priority Non-Preemptive Scheduling:")
    print(f"Average Turnaround Time: {avg_tat:.2f}")
    print(f"Average Waiting Time: {avg_wt:.2f}")
    print(f"Average Response Time: {avg_rt:.2f}")
    return{"chart" :gantt,
            "processes":PID_arr,
            "priorities":PRI_arr,
            "turnaround_time":TAT_arr,
            "waiting_time":WT_arr,
            "response_time":RT_arr,
            "avg_turnaround_time":avg_tat,
            "avg_waiting_time":avg_wt,
            "avg_response_time":avg_rt}
  
  def priority_preemptive(process_list):
    # [AT, BT, PID, Priority]
    # If no arrival time is provided, set all arrival times to 0
    for process in process_list:
        if len(process) == 3:  # If only 3 elements (AT, BT, PID) are provided
            process.insert(0, 0)  # Set Arrival Time (AT) to 0 at the beginning

        if len(process) == 4:
            process.insert(4, -1)  # Add placeholder for Start Time (ST) if missing

    t = 0  # Current time
    gantt = []  # To store the Gantt chart representation of process execution
    completed = {}  # Dictionary to store completion details of each process
    response_times = {}  # Dictionary to store response times of processes

    original_bt = {p[2]: p[1] for p in process_list}  # Store original burst times

    while process_list:
        # Filter processes that have arrived
        available = [p for p in process_list if p[0] <= t]

        if not available:
            # If no processes are available, the CPU is idle
            gantt.append("Idle")
            t += 1
            continue

        # Sort by priority, then by arrival time
        available.sort(key=lambda x: (x[3], x[0]))
        process = available[0]  # Select the process with the highest priority

        if process[4] == -1:  # Start Time has not been set
            # Record response time for the first execution
            response_times[process[2]] = t - process[0]  # Response Time = Start Time - Arrival Time
            process[4] = t  # Set Start Time (ST)

        if len(gantt) > 0 and gantt[-1]["name"] == str(process[2]):
          gantt[-1]["interval"][1] = t+1
        else:
          gantt.append({"name": str(process[2]), "interval":[t, t+1]})  # Add the process ID to the Gantt chart
        process[1] -= 1  # Decrease burst time by 1 (executing for 1 time unit)
        t += 1  # Increment time

        if process[1] == 0:
            # If the process has completed execution
            CT = t  # Completion Time
            AT = process[0]  # Arrival Time
            BT = original_bt[process[2]]  # Use the original Burst Time
            ST = process[4]  # Start Time
            TAT = CT - AT  # Turnaround Time = Completion Time - Arrival Time
            WT = TAT - BT  # Waiting Time = Turnaround Time - Burst Time

            completed[process[2]] = [process[3], AT, BT, ST, CT, TAT, WT]
            process_list.remove(process)  # Remove the completed process

    # Print Gantt Chart
    # print("Gantt Chart:", gantt)

    # Print Process Details
    # print("\nPriority Preemptive Process Details:")
    # print("Process\tPri\tAT\tBT\tST\tCT\tTAT\tWT\tRT")

    total_tat = 0  # Total Turnaround Time
    total_wt = 0  # Total Waiting Time
    total_rt = 0  # Total Response Time
    n = len(completed)  # Number of processes
    PID_arr=[]
    PRI_arr=[]
    AT_arr=[]
    BT_arr=[]
    ST_arr=[]
    CT_arr=[]
    TAT_arr=[]
    WT_arr=[]
    RT_arr=[]

    for pid, details in completed.items():
        priority_value, arrival_time, burst_time, start_time, ct, tat, wt = details
        rt = response_times[pid]  # Retrieve response time for the process
        total_tat += tat  # Accumulate Turnaround Time
        total_wt += wt  # Accumulate Waiting Time
        total_rt += rt  # Accumulate Response Time
        # print(f"{pid}\t{priority_value}\t{arrival_time}\t{burst_time}\t{start_time}\t{ct}\t{tat}\t{wt}\t{rt}")
        PID_arr.append(pid)
        PRI_arr.append(priority_value)
        AT_arr.append(arrival_time)
        BT_arr.append(burst_time)
        ST_arr.append(start_time)
        CT_arr.append(ct)
        TAT_arr.append(tat)
        WT_arr.append(wt)
        RT_arr.append(rt)

    # Calculate Averages
    avg_tat = total_tat / n  # Average Turnaround Time
    avg_wt = total_wt / n  # Average Waiting Time
    avg_rt = total_rt / n  # Average Response Time

    # print("\nAverages for Priority Preemptive Scheduling:")
    # print(f"Average Turnaround Time: {avg_tat:.2f}")
    # print(f"Average Waiting Time: {avg_wt:.2f}")
    # print(f"Average Response Time: {avg_rt:.2f}")
    return{"chart" :gantt,
            "processes":PID_arr,
            "priorities":PRI_arr,
            "turnaround_time":TAT_arr,
            "waiting_time":WT_arr,
            "response_time":RT_arr,
            "avg_turnaround_time":avg_tat,
            "avg_waiting_time":avg_wt,
            "avg_response_time":avg_rt}