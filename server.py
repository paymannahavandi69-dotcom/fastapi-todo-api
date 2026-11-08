from fastapi import FastAPI , HTTPException
from pydantic import BaseModel 

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str
    done: bool = False

tasks = [
    Task(id=1, title="Learn Python", done=True),
    Task(id=2, title="Learn FastAPI", done=False)
]

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return {"message": "Task added", "task": task}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return {"message": f"Task {task_id} deleted"}
    raise HTTPException(status_code=404, detail="Task not found")