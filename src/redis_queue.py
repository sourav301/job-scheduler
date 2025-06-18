from job_store import JobStore
from database import session
from datetime import datetime, timezone
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)
zset_key = "job_queue"
    
def add_job_to_redis_queue(job, priority=100):
    redis_client.zadd(zset_key, {f"job:{job.id}": priority})

def get_top_job():
    result = redis_client.zrange("job_queue", 0, 0, withscores=True)

    if result:
        return result[0]
    return None
if __name__=="__main__":
     
    # Read back the data (ascending order by score)
    print("Jobs in queue (by score):")
    

    # job_store = JobStore(session)
    # pending = job_store.get_due_jobs(datetime.now(timezone.utc))
    # for job in pending:
    #     print(f"Job ID: {job.id}, Name: {job.name}, Run At: {job.run_at}, Status: {job.status}")
    #     redis_client.zadd(zset_key, {f"job:{job.id}": 100})
    # print(get_top_job())

    