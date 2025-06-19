from fastapi import FastAPI, Depends
from typing import List
from uuid import UUID 
from models import Job
from job_store import JobStore
from schema import JobCreate, JobRead, JobReadMin
from database import get_db, SessionLocal  
from sqlalchemy.orm import Session
import asyncio
from contextlib import asynccontextmanager
from strategies import  SJF_SchedulerStrategy
from scheduler import JobScheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Start loop to add job to redis'''
    strategy = SJF_SchedulerStrategy()
    job_scheduler = JobScheduler(strategy,db=SessionLocal())
    task = asyncio.create_task(job_scheduler.scheduler_loop())
    yield
    task.cancel() 

app = FastAPI(lifespan=lifespan)

@app.post("/jobs", response_model=JobRead)
def create_job(job: JobCreate,  db: Session = Depends(get_db)):
    '''Create new job in database'''
    db_job = Job(
        name = job.name,
        cron_expression=job.cron_expression,
        run_at=job.run_at,
        estimated_runtime = job.estimated_runtime,
        parameters = job.parameters
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/jobs/{job_id}", response_model=JobRead)
def get_job(job_id: UUID,  db: Session = Depends(get_db)):
    '''Get particular job details'''
    job_store = JobStore(db)
    return job_store.get_job(job_id)


@app.get("/jobs", response_model=List[JobReadMin])
def get_job( db: Session = Depends(get_db)):
    '''Get all job details in brief'''
    print("getting all job")
    job_store = JobStore(db)
    return job_store.get_all_jobs()

