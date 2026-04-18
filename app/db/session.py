from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_config




settings = get_config()
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker[Session](bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()