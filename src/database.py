from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# Replace with your Postgres DB URL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/scheduler"

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