from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from schedulers import Schedulers

class Process(BaseModel):
  burst_time: int
  arrival_time: int | None = 0
  id: int
  priority: int | None = 0

class ProcessList(BaseModel):
  processes: List[Process]
  time_quanta: int | None = 99999999999

app = FastAPI()

app.mount("/static", StaticFiles(directory="static",html = True), name="static")

@app.post("/api/test/")
def test(processes: ProcessList):
  return {
    "chart": [{"name": "1", "interval": [0, 1]}, {"name": "2", "interval": [1, 5]}, {"name": "3","interval": [5, 12]}, {"name": "4", "interval": [12, 14]}],
    "waiting_time": [0, 1, 5, 12],
    "response_time": [0, 1, 5, 12],
    "turnaround_time": [1, 5, 12, 14]
    }

@app.post("/api/simulate/sjf/non-preemptive")
  # [arrival time, burst time, process id]
def sjf_non_preemptive(processes: ProcessList):
  process_list = []
  for process in processes.processes:
    process_list.append([process.arrival_time, process.burst_time, process.id])
  results = Schedulers.simulate(algo_name="SJF_non_preemptive", processes_list=process_list)
  return results

@app.post("/api/simulate/sjf/preemptive")
def sjf_preemptive(processes: ProcessList):
  return {"status": "not implemented yet"}

@app.post("/api/simulate/fcfs")
  # [arrival time, burst time, proccess id]
def fcfs(processes: ProcessList):
  process_list = []
  for process in processes.processes:
    process_list.append([process.arrival_time, process.burst_time, process.id])
  results = Schedulers.simulate(algo_name="fcfs", processes_list=process_list)
  return results

@app.post("/api/simulate/round-robin")
def round_robin(processes: ProcessList):
  if processes.time_quanta <= 0:
    processes.time_quanta = 99999999999
  process_list = []
  for process in processes.processes:
    process_list.append([process.arrival_time, process.burst_time, process.id])
  results = Schedulers.simulate(algo_name="round_robin", processes_list=process_list, time_quanta=processes.time_quanta)
  return results

@app.post("/api/simulate/priority/non-preemptive")
def priority_non_preemptive(processes: ProcessList):
  process_list = []
  for process in processes.processes:
    process_list.append([process.arrival_time, process.burst_time, process.id, process.priority])
  results = Schedulers.simulate(algo_name="Priority_Non_Preemptive", processes_list=process_list)
  return results

@app.post("/api/simulate/priority/preemptive")
def priority_preemptive(processes: ProcessList):
  return {"status": "not implemented yet"}