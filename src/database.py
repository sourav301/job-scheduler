from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import DATABASE_URL

# Create DB engine and session
engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine) 
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()