from fastapi import APIRouter
from app.queue.tasks import add_task

router = APIRouter()

@router.get("/add")
def add(a: int, b: int):
    task = add_task.delay(a, b)
    return {"task_id": task.id}