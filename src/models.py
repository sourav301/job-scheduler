'''Describes SQLAlchemy ORM object for job scheduler'''

import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String,Integer, DateTime, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base

class JobStatus(str, enum.Enum):
    '''Enum for All possible stages'''
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
class JobType(str, enum.Enum):
    '''Type of job whether recurring on onetime'''
    ONETIME = "ONETIME"
    RECURRING = "RECURRING"
    
class Job(Base):
    __tablename__ = 'jobs'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    job_type = Column(Enum(JobType), default = JobType.ONETIME)
    cron_expression = Column(String, nullable=True)
    run_at = Column(DateTime(timezone=True), nullable = True)
    estimated_runtime = Column(Integer, nullable = False)
    parameters = Column(JSON)
    status = Column(Enum(JobStatus),default=JobStatus.PENDING)
    last_successful_run = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))