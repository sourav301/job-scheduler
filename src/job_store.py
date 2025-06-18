from sqlalchemy.orm import Session
from models import Job,JobStatus, Base
from datetime import datetime, timedelta, timezone
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
    
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
if __name__=="__main__":

    start_time = datetime.now(timezone.utc) + timedelta(minutes=1)
    job_data = {"name":"my_other", 
                     "cron_expression":"1 2 * * *",
                     "run_at" : start_time,
                     "parameters":{"path":"/home/user/job_file_1"}
}
     
    
    # Replace with your Postgres DB URL
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/scheduler"
    
    # Create DB engine and session
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    job_store = JobStore(session)
    res = job_store.add_job(job_data)
    
    print(res)