from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
from datetime import datetime, timedelta
from src.config import DATABASE_URL
from src.logger import AppLogger

logger = AppLogger()
# Create DB engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine) 
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 