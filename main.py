from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

class Process(BaseModel):
  burst_time: int
  arrival_time: int | None = 0
  id: int
  priority: int | None = 0

class ProcessList(BaseModel):
  processes: List[Process]
  time_quanta: int | None = 0

app = FastAPI()

app.mount("/static", StaticFiles(directory="static",html = True), name="static")

@app.post("/api/test/")
def add_loan(processes: ProcessList):
  return {
    "chart": [{"name": "1", "interval": [0, 1]}, {"name": "2", "interval": [1, 5]}, {"name": "3","interval": [5, 12]}, {"name": "4", "interval": [12, 14]}],
    "waiting_time": [0, 1, 5, 12],
    "response_time": [0, 1, 5, 12],
    "turnaround_time": [1, 5, 12, 14]
    }