from sqlalchemy.orm import Session
from models import Job,JobStatus
from datetime import datetime,  timezone 
from database import get_db
from logger import AppLogger

logger = AppLogger()

class JobStore:

    def __init__(self, db_session: Session):
        self.db = db_session
    
    def add_job(self,job_data):
        job = Job(**job_data)
        self.db.add(job)
        self.db.commit()
        return job
    
    def update_run_at(self,job_id,run_at):
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if job and run_at:
            job.run_at=run_at
            self.db.commit()
            logger.info("run_at updated")
    
    def update_status(self,job_id,status):
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if job and status:
            job.status=status
            self.db.commit()
            logger.info("status updated")

    def get_due_jobs(self, now):
        return self.db.query(Job).filter(Job.run_at <=now, Job.status==JobStatus.PENDING).all()
    
    def get_job(self, job_id):
        return self.db.query(Job).filter(Job.id == job_id).first()

    def get_all_jobs(self):
        return self.db.query(Job)

    
if __name__=="__main__":
    session = get_db()
    start_time = datetime.now(timezone.utc)  
    job_data = {"name":"my_job", 
                     "cron_expression":"1 * * * *",
                     "run_at" : start_time,
                     "estimated_runtime" : 120,
                     "parameters":{"path":"/home/user/job_file_1"}
    }
      
    job_store = JobStore(session)
    res = job_store.add_job(job_data)
    
    job_data = {"name":"my_other_job", 
                     "cron_expression":"1 2 * * *",
                     "run_at" : start_time,
                     "estimated_runtime" : 10,
                     "parameters":{"path":"/home/user/job_file_1"}
    }
      
    job_store = JobStore(session)
    res = job_store.add_job(job_data)
    
    jobs = job_store.get_due_jobs(datetime.now(timezone.utc))
    for job in jobs:
        logger.info(f"Job ID: {job.id}, Name: {job.name}, Run At: {job.run_at}, Status: {job.status}")