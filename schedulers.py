class Schedulers:
  # def __init__(self, value):
  #   self.value = value

  def simulate(algo_name: str, processes_list, time_quanta=0):
    match algo_name:
        case "SJF_non_preemptive":
            return Schedulers.SJF_non_preemptive(processes_list)
        case "fcfs":
            # return fcfs(processes_list)
            return "not implemented yet"
        case "round_robin":
            return "not implemented yet"
            # return round_robin(processes_list, time_quanta)
        case "Priority_Non_Preemptive":
            return "not implemented yet"
            # return priority(processes_list)
        case "priority_preemptive" :
            return "not implemented yet"
            # return priority_preemptive(processes_list)
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
            "Average Turnaround time":sum(TT) / len(TT) ,
            "Average Waiting time": sum(WT) / len(WT),
            "Average Response time": sum(WT) / len(WT)
            }