from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
# Replace with your Postgres DB URL
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/scheduler"

# Create DB engine and session
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
