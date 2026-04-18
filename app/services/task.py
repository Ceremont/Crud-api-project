from fastapi import HTTPException

from app.repositories.task import TaskRepository
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskUpdate,Task

class TaskService:
    def __init__(self,db:Session) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)

    def list_tasks(self) -> list[Task]:
        task_orm = self.task_repository.get_all()
        return [Task.model_validate(task) for task in task_orm]

    def create_task(self,task_create: TaskCreate) -> Task:
        task_orm = self.task_repository.create(title=task_create.title)
        self.db.commit()
        return Task.model_validate(task_orm)

    def update_task(self,task_id:str,task_update: TaskUpdate) -> Task:
        task_for_update = self.task_repository.get_by_id(task_id = task_id)
        if task_for_update is None:
            raise HTTPException(status_code=404, detail="Task not found")
        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed

        self.db.commit()
        return Task.model_validate(task_for_update)

    def delete_task(self,task_id:str) -> Task:
        task_for_delete = self.task_repository.get_by_id(task_id = task_id)
        self.task_repository.delete(task_for_delete)
        self.db.commit()