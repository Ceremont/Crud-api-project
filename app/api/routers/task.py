from fastapi import APIRouter,status
from fastapi.params import Depends

from app.api.dependencies import get_task_service
from app.schemas.task import TaskUpdate, TaskCreate, Task
from app.services.task import TaskService

router = APIRouter(prefix="/tasks")


@router.get("")
def read_tasks(task_service: TaskService = Depends(get_task_service)) -> list[Task]:
    return task_service.list_tasks()

@router.post("",status_code=status.HTTP_201_CREATED)
def create_tasks(payload:TaskCreate,task_service: TaskService = Depends(get_task_service)) -> Task:
    return task_service.create_task(task_create=payload)

@router.patch("/{task_id}")
def update_tasks(task_id: str, payload: TaskUpdate,task_service: TaskService = Depends(get_task_service)) -> Task:
    return task_service.update_task(task_id = task_id,task_update=payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tasks(task_id:str,task_service: TaskService = Depends(get_task_service)):
    return task_service.delete_task(task_id=task_id)