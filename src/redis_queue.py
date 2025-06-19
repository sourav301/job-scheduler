from job_store import JobStore 
from datetime import datetime, timezone
import redis
from logger import AppLogger

logger = AppLogger()

redis_client = redis.Redis(host='localhost', port=6379, db=0)
zset_key = "job_queue"
    
def add_job_to_redis_queue(job, priority=100):
    try:
        redis_client.zadd(zset_key, {f"job:{job.id}": priority})
    except redis.RedisError as e:
        logger.error(f"Failed to add Job:{job.id} with priority {priority} to redis: {e}")
        raise
def get_top_job():
    try:
        result = redis_client.zrange("job_queue", 0, 0, withscores=True)
        if result:
            return result[0]
        return None
    except redis.RedisError as e:
        logger.error(f"Failed to get top job from redis: {e}")
        raise