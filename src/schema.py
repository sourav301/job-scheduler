'''Pydantic models for request and response schemas used by 
the job scheduler API'''

from uuid import UUID
from datetime import datetime 
from typing import Optional, Any, Dict
from pydantic import BaseModel
from src.models import JobStatus, JobType

class JobCreate(BaseModel):
    '''Create a job'''
    name: str 
    job_type: Optional[JobType] = JobType.ONETIME
    cron_expression: Optional[str] = None
    run_at: Optional[datetime] = None
    estimated_runtime: int
    parameters: Dict[str, Any]  

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Data Backup Job",
                "cron_expression": "0 0 * * *",
                "job_type": "ONETIME",
                "run_at": "2025-06-18T16:00:00Z",
                "estimated_runtime": 30,
                "parameters": {"location": "/mnt/backup"}
            }
        }

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

 