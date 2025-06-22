'''Pydantic models for request and response schemas used by 
the job scheduler API'''

from uuid import UUID
from datetime import datetime, timezone
from typing import Optional, Any, Dict
from pydantic import BaseModel, Field
from src.models import JobStatus, JobType


class JobCreate(BaseModel):
    """
    Request model to create a job.
    """
    name: str = Field(..., description="Name of the job", example="Number Crunching Job")
    job_type: Optional[JobType] = Field(
        default=JobType.ONETIME, 
        description="Type of the job: ONETIME or RECURRING",
        example="ONETIME"
    )
    cron_expression: Optional[str] = Field(
        default=None, 
        description="Cron expression for recurring jobs. Required if job_type is RECURRING.",
        example="* * * * *"
    )
    run_at: Optional[datetime] = Field(
        default=None, 
        description="Scheduled time for jobs in ISO format (UTC).",
        example=datetime.now(timezone.utc)
    )
    estimated_runtime: int = Field(
        ..., 
        description="Estimated runtime in seconds", 
        example=30
    )
    parameters: Dict[str, Any] = Field(
        ..., 
        description="Dictionary of parameters required by the job", 
        example={"service":"my-service","source": "s3://my-bucket"}
    )
    class Config:
        orm_mode = True 

class JobRead(BaseModel):
    '''All details for a job'''
    id: UUID
    name: str
    job_type: Optional[JobType] = JobType.ONETIME
    cron_expression: Optional[str] = None
    run_at: Optional[datetime] = None
    estimated_runtime: int
    parameters: Any
    status: JobStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class JobReadMin(BaseModel):
    '''Used while returning list of all jobs'''
    # id: UUID
    name: str
    # cron_expression: Optional[str] = None
    run_at: Optional[datetime] = None
    estimated_runtime: int
    # parameters: Any
    # status: JobStatus
    # created_at: datetime
    # updated_at: datetime

    class Config:
        orm_mode = True

class JobUpdateStatus(BaseModel):
    '''For updating the job status'''
    status: JobStatus

    class Config:
        orm_mode = True

 