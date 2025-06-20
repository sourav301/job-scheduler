'''Implementation of shortest job first with ageing'''
from job_store import JobStore
from models import JobStatus, Job 
from datetime import datetime, timezone, timedelta
from redis_queue import RedisClient 
import redis
from croniter import croniter
import time  
import asyncio
from strategies import SchedulerStrategy
from logger import AppLogger 
from redis_queue import RedisClient
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
        logger.info(f"No. of pending jobs: {len(pending)}")
        
        for job in pending:
            # self.update_next_run(job.id, job.cron_expression)
            now = datetime.now(timezone.utc) 

            # Loop over jobs that should have started in the last 1 min
            if abs(job.run_at-now)<timedelta(days=1) and job.status==JobStatus.PENDING:
                self.schedule_jobs(now, job)

    def schedule_jobs(self, now, job):
        score = self.scheduler_strategy.calculate_score(job)
        self.redis_client.add_to_list({f"job:{job.id}": score})
        self.job_store.update_status(job.id,JobStatus.SCHEDULED)
        logger.info(f"Schedule,{abs(job.run_at-now)}")

    def update_next_run(self,job_id, cron_expression):
        '''Evaluate cron expression for completed job and update run_at column'''
        
        now = datetime.now(timezone.utc)
        cron = croniter(cron_expression,now)
        next = cron.get_next(datetime)
        self.job_store.update_run_at(job_id,next)
        logger.info(f"{job_id}: Next run scheduled at {next}")
        
    def execute_job(self):
        '''Execute highest priority job'''
        job_id = self.redis_client.get_top_job() 
        if job_id is None:
            return
        job = self.job_store.get_job(job_id)
        logger.info(f"Executing job: {job_id}: Estimated runtime: {job.estimated_runtime}") 
        time.sleep(3)
        logger.info("Execution completed") 
        self.job_store.update_status(job_id,JobStatus.COMPLETED)
        

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
        logger.info("Scheduler loop")
        i=0
        while True:
            logger.info(f"Executor loop: {i}") 
            await asyncio.get_event_loop().run_in_executor(None,  self.execute_job)
            await asyncio.sleep(3)
            i+=1 
            