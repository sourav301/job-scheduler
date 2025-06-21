from fastapi import FastAPI, Depends
from typing import List
from uuid import UUID 
import asyncio
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from src.models import Job
from src.strategies import  SJF_SchedulerStrategy
from src.scheduler import JobScheduler
from src.job_store import JobStore
from src.schema import JobCreate, JobRead, JobReadMin
from src.database import get_db, SessionLocal, engine, Base 

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Start loop to add job to redis'''
    Base.metadata.create_all(bind=engine)
    strategy = SJF_SchedulerStrategy()
    # Job scheduler 
    job_scheduler = JobScheduler(strategy,db=SessionLocal())
    scheduler_task = asyncio.create_task(job_scheduler.scheduler_loop())
    # Job executor 
    executor_task = asyncio.create_task(job_scheduler.executor_loop())
    yield
    scheduler_task.cancel() 
    executor_task.cancel() 

app = FastAPI(lifespan=lifespan)

@app.post("/jobs", response_model=JobRead)
def create_job(job: JobCreate,  db: Session = Depends(get_db)):
    '''Create new job in database'''
    db_job = Job(
        name = job.name,
        job_type=job.job_type,
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

