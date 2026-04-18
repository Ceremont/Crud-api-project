from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_config
from app.models.base import Base
from app.db.session import engine
from app.api.routers.task import router as task_router

config = get_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    print("App closed")


app = FastAPI(lifespan=lifespan)
app.include_router(task_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

