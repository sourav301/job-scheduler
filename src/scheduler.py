'''Schedule jobs by following the following steps.
1. Gets pending jobs from datatbase.
2. Calculate score or priority of job.
3. Pushes job to redis list.
4. Gets job with lowest score for execution.
5. Update status of job in database - SCHEDULED, COMPLETED, etc
 '''
from datetime import datetime, timezone, timedelta
from croniter import croniter
import time  
import asyncio
from src.redis_queue import RedisClient 
from src.strategies import SchedulerStrategy
from src.logger import AppLogger 
from src.redis_queue import RedisClient
from src.job_store import JobStore
from src.models import JobStatus, JobType 

logger = AppLogger()

class JobScheduler:
    
    def __init__(self, scheduler_strategy: SchedulerStrategy, db):
        self.redis_client = RedisClient()
        self.scheduler_strategy = scheduler_strategy
        self.job_store = JobStore(db)
        self.db = db

    def schedule_pending_jobs(self):
        '''Schedule if the job was scheduled to be run in last 1 min and still in pending'''
        pending = self.job_store.get_due_jobs(datetime.now(timezone.utc))
        if len(pending)>0:
            logger.info(f"No. of pending jobs: {len(pending)}")
        
        for job in pending:
            
            now = datetime.now(timezone.utc) 

            # Loop over jobs that should have started by now
            if job.run_at<now and job.status==JobStatus.PENDING:
                self.schedule_jobs(now, job)

    def schedule_jobs(self, now, job):
        score = self.scheduler_strategy.calculate_score(job)
        self.redis_client.add_to_list({f"job:{job.id}": score})
        self.job_store.update_status(job.id,JobStatus.SCHEDULED)

    def update_next_run(self,job_id):
        '''Evaluate cron expression for completed job and update run_at column'''
        job = self.job_store.get_job(job_id) 
        if job:
            now = datetime.now(timezone.utc)
            cron = croniter(job.cron_expression,now)
            next = cron.get_next(datetime)
            self.job_store.update_run_at(job_id,next)
            logger.info(f"Scheduler: {job_id}: Next run scheduled at {next}")
        
    def execute_job(self):
        '''Execute highest priority job'''
        job_id = self.redis_client.get_top_job() 
        if job_id is None:
            return
        job = self.job_store.get_job(job_id)
        if not job:
            logger.error(f"Executing job: Not found: {job_id} ")
            return 
        logger.info(f"Executing job: {job_id}: Estimated runtime: {job.estimated_runtime}") 
        time.sleep(job.estimated_runtime)
        logger.info("Execution completed") 

        if job.job_type==JobType.ONETIME:
            self.job_store.update_status(job_id,JobStatus.COMPLETED)
            
        elif job.job_type==JobType.RECURRING:
            self.job_store.update_status(job_id,JobStatus.PENDING)
            self.update_next_run(job_id)

        self.job_store.update_successful_run(job_id,datetime.now(timezone.utc))
        

    async def scheduler_loop(self):
        '''Every 1 min selects jobs from the database and add to redis.'''
        logger.info("Scheduler loop")
        i = 0 
        while True:   
            await asyncio.get_event_loop().run_in_executor(None, self.schedule_pending_jobs)
            # logger.info(f"Scheduler loop: {i}")
            await asyncio.sleep(3)
            i+=1

    async def executor_loop(self):
        '''Poll jobs from redis and execute'''
        logger.info("Executor loop")
        i=0
        while True:
            logger.info(f"Executor loop: {i}") 
            await asyncio.get_event_loop().run_in_executor(None,  self.execute_job)
            await asyncio.sleep(3)
            i+=1 
            
# if __name__=="__main__":
#     from src.strategies import SJF_SchedulerStrategy
#     from src.database import get_db
#     db = next(get_db())
#     job_scheduler = JobScheduler(SJF_SchedulerStrategy, db)
#     job_scheduler.update_next_run("5ee6c90e-6a91-40cb-8683-d7238101afc5")
    
#     job_store = JobStore(db) 
#     job_store.update_run_at("5ee6c90e-6a91-40cb-8683-d7238101afc5",datetime.now(timezone.utc))

