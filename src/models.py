from sqlalchemy import Column, String,Integer, DateTime, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    cron_expression = Column(String, nullable=True)
    run_at = Column(DateTime, nullable = True)
    estimated_runtime = Column(Integer, nullable = False)
    parameters = Column(JSON)
    status = Column(Enum(JobStatus),default=JobStatus.PENDING)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))