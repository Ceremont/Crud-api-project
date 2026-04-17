from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.testing.schema import mapped_column
from starlette import status
from fastapi import HTTPException
from sqlalchemy import create_engine,select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, Session

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker[Session](bind=engine)

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True,default=lambda: str(uuid4()))


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    print("App closed")

class TaskORM(Base):
    __tablename__ = "tasks"

    title:Mapped[str]
    completed:Mapped[bool] = mapped_column(default=False)



app = FastAPI(lifespan=lifespan)

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

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

def task_to_model(task_orm:TaskORM) -> Task:
    return Task(id=task_orm.id, title=task_orm.title, completed=task_orm.completed)

@app.get("/tasks")
def read_tasks(db: Session  = Depends(get_db)) -> list[Task]:
    tasks = db.scalars(select(TaskORM)).all()
    return [task_to_model (task) for task in tasks]

@app.post("/tasks",status_code=status.HTTP_201_CREATED)
def create_tasks(payload:TaskCreate,db: Session  = Depends(get_db)) -> Task:
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()

    return task_to_model(new_task)

@app.patch("/tasks/{task_id}")
def update_tasks(task_id: str, payload: TaskUpdate,db: Session  = Depends(get_db)) -> Task:
    task_for_update = db.get(TaskORM,task_id)
    if task_for_update is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if payload.title:
        task_for_update.title = payload.title
    if payload.completed:
        task_for_update.completed = payload.completed

    db.commit()
    return task_for_update


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tasks(task_id:str,db: Session  = Depends(get_db)):
    task_for_delete = db.get(TaskORM,task_id)
    if task_for_delete is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_for_delete)
    db.commit()
