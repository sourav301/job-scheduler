'''Implementation of shortest job first with ageing'''
from job_store import JobStore
from models import JobStatus, Job 
from datetime import datetime, timezone, timedelta
from redis_queue import get_top_job 
import redis
from croniter import croniter
import time  
import asyncio
from strategies import SchedulerStrategy
from logger import AppLogger

logger = AppLogger()

       
class JobScheduler:
    
    def __init__(self, scheduler_strategy: SchedulerStrategy, db):
        
        self.scheduler_strategy = scheduler_strategy
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.zset_key = "job_queue"
        self.job_store = JobStore(db)


    def schedule_pending_jobs(self):
        '''Schedule if the job was scheduled to be run in last 1 min and still in pending'''
        pending = self.job_store.get_due_jobs(datetime.now(timezone.utc))
        logger.info(f"Checking pending jobs: {len(pending)}")
        
        for job in pending:
            self.update_next_run(job.id, job.cron_expression)
            # logger.info(f"\n\n{job.cron_expression}, Name: {job.name}, Run At: {job.run_at}, Status: {job.status}, Runtime: {job.estimated_runtime}")
            now = datetime.now(timezone.utc) 
            logger.info( abs(job.run_at-now)<timedelta(days=5)and job.status==JobStatus.PENDING )
            if abs(job.run_at-now)<timedelta(minutes=1) and job.status==JobStatus.PENDING:
                
                logger.info(f"Schedule,{abs(job.run_at-now)}")
                score = self.scheduler_strategy.calculate_score(job)
                self.redis_client.zadd(self.zset_key, {f"job:{job.id}": score})
                self.job_store.update_status(job.id,JobStatus.SCHEDULED)

    def update_next_run(self,job_id, cron_expression):
        '''Evaluate cron expression for completed job and update run_at column'''
        logger.info(f"inside update_next_run{cron_expression}")
 
        now = datetime.now(timezone.utc)
        cron = croniter("* * * * *",now)
        next = cron.get_next(datetime)
        self.job_store.update_run_at(job_id,next)
        logger.info(f"{job_id} next run at {next}")
        
    def execute_job(self):
        '''Fetch highest priority job'''
        job = get_top_job()
        logger.info("Executing job")
        logger.info(job)
        time.sleep(2)
        logger.info("execution completed")
        #update database
        

    async def scheduler_loop(self):
        '''Every 1 min selects jobs from the database and add to redis.'''
        logger.info("Scheduler loop")
        i = 0 
        while True:   
            await asyncio.get_event_loop().run_in_executor(None, self.schedule_pending_jobs)
            logger.info(f"Started scheduler loop: {i}")
            await asyncio.sleep(2)
            i+=1