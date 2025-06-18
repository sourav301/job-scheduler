'''Implementation of shortest job first with ageing'''
from job_store import JobStore
from models import JobStatus
from database import session
from datetime import datetime, timezone, timedelta
import redis
from croniter import croniter

redis_client = redis.Redis(host='localhost', port=6379, db=0)
zset_key = "job_queue"
job_store = JobStore(session)

def schedule_pending_jobs():
    '''Schedule if the job was scheduled to be run in last 1 min and still in pending'''
    
    pending = job_store.get_due_jobs(datetime.now(timezone.utc))
    for job in pending:
        print(f"\n\n{job.cron_expression}, Name: {job.name}, Run At: {job.run_at}, Status: {job.status}, Runtime: {job.estimated_runtime}")
        now = datetime.now(timezone.utc)
        if abs(job.run_at-now)<timedelta(days=30) and job.status==JobStatus.PENDING:
            print("Schedule,",abs(job.run_at-now))
            redis_client.zadd(zset_key, {f"job:{job.id}": job.estimated_runtime})

def update_next_run(job_id):
    '''Evaluate cron expression for completed job and update run_at column'''

    job = job_store.get_job(job_id)
    now = datetime.now(timezone.utc)
    cron = croniter(job.cron_expression,now)
    next = cron.get_next(datetime)
    job_store.update_run_at(job,next)
    

def update_scores():
    '''Apply ageing: Reduce scores of existing jobs'''

    r = redis.Redis(host='localhost', port=6379, db=0)
    lua_script = """
    local key = KEYS[1]
    local members = redis.call('ZRANGE', key, 0, -1)
    for i=1,#members do
    redis.call('ZINCRBY', key, -1, members[i])
    end
    return true
    """

    r.eval(lua_script, 1, zset_key)

if __name__=="__main__":
    # schedule_pending_jobs()
    # update_scores()
    # update_next_run('cade7f2c-6063-4ccf-a72a-8fce4f2d5b5f') 
    