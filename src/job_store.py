from sqlalchemy.orm import Session
from models import Job,JobStatus
from datetime import datetime, timedelta, timezone
from database import session

class JobStore:

    def __init__(self, db_session: Session):
        self.db = db_session
    
    def add_job(self,job_data):
        job = Job(**job_data)
        self.db.add(job)
        self.db.commit()
        return job
    
    def get_due_jobs(self, now):
        return self.db.query(Job).filter(Job.run_at <=now, Job.status==JobStatus.PENDING).all()
    
if __name__=="__main__":

    start_time = datetime.now(timezone.utc) + timedelta(minutes=1)
    job_data = {"name":"my_other_job", 
                     "cron_expression":"1 2 * * *",
                     "run_at" : start_time,
                     "estimated_runtime" : 60,
                     "parameters":{"path":"/home/user/job_file_1"}
    }
     
    
    
    job_store = JobStore(session)
    res = job_store.add_job(job_data)
    jobs = job_store.get_due_jobs(datetime.now(timezone.utc))
    for job in jobs:
        print(f"Job ID: {job.id}, Name: {job.name}, Run At: {job.run_at}, Status: {job.status}")