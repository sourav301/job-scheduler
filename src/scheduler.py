from job_store import JobStore
from database import session
from datetime import datetime, timezone
import redis
from croniter import croniter

redis_client = redis.Redis(host='localhost', port=6379, db=0)
zset_key = "job_queue"
     

if __name__=="__main__":
     
    # Read back the data (ascending order by score)
    print("Jobs in queue (by score):")
    

    job_store = JobStore(session)
    pending = job_store.get_due_jobs(datetime.now(timezone.utc))
    for job in pending:
        print(f"{job.cron_expression}, Name: {job.name}, Run At: {job.run_at}, Status: {job.status}, Runtime: {job.estimated_runtime}")
        now = datetime.now(timezone.utc)
        cron = croniter(job.cron_expression,now)
        last = cron.get_prev(datetime)
        
        print("last run at ", last)
        print("delay", now-last)
        # redis_client.zadd(zset_key, {f"job:{job.id}": 100})
     

    