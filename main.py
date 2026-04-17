from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from fastapi import HTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Task(BaseModel):
    id:str
    title:str
    completed:bool

class TaskCreate(BaseModel):
    title:str

class TaskUpdate(BaseModel):
    title:str | None  = None
    completed:bool | None  = None


tasks: list[Task] = []

@app.get("/tasks")
def read_tasks() -> list[Task]:
    return tasks

@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_tasks(payload:TaskCreate) -> Task:
    new_task = Task(id =str(uuid4()), title = payload.title, completed = False)
    tasks.append(new_task)
    return new_task

@app.patch("/tasks/{task_id}")
def update_tasks(task_id: str, payload: TaskUpdate) -> Task:
    for task in tasks:
        if task.id == task_id:
            if payload.title is not None:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task

    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tasks(task_id:str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
