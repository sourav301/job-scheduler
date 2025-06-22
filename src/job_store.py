import functools
from sqlalchemy.orm import Session
from src.models import Job,JobStatus
from datetime import datetime,  timezone 
from src.database import get_db
from src.logger import AppLogger

logger = AppLogger()

class JobStore:

    def __init__(self, db_session: Session):
        self.db = db_session

    def db_transaction(func):
        '''Decorator to wrap database operations in a transaction
        Args:
            func (Callable): The repository method to wrap.
        Returns:
            Callable: Wrapped function with automatic transaction management.
        Raises:
            Propagates any exception after rolling back the transaction.'''
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self,*args,**kwargs)
                self.db.commit()
                return result
            except Exception as e:
                self.db.rollback()
                logger.error(f"Database error in {func.__name__}: {e}")
                raise 
        return wrapper

    @db_transaction
    def add_job(self,job_data):
        job = Job(**job_data)
        self.db.add(job) 
        return job

    def __update_fields(self, job_id, update_dict):
        '''Private method to update model data'''
        updated_rows = self.db.query(Job).filter(Job.id == job_id).update(update_dict)
        if updated_rows:
            logger.info(f"Database: {job_id} update {' '.join(list(update_dict.keys()))}")
        else:
            logger.warning(f"Database: {job_id} not found")

    @db_transaction
    def update_run_at(self,job_id,run_at): 
        return self.__update_fields(job_id, {"run_at":run_at})

    @db_transaction
    def update_status(self,job_id,status):
        return self.__update_fields(job_id, {"status":status})


    @db_transaction
    def update_successful_run(self,job_id, time):
        return self.__update_fields(job_id, {"last_successful_run":time})


    def get_due_jobs(self, now):
        return self.db.query(Job).filter(Job.run_at <=now, Job.status==JobStatus.PENDING).all()
    
    def get_job(self, job_id):
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if job:
            return job
        else:
            logger.info(f"Database: {job_id} is not found")
            return None

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
        logger.info(f"Database: Job ID: {job.id}, Name: {job.name}, Run At: {job.run_at}, Status: {job.status}")