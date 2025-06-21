import redis
from src.logger import AppLogger
from src.config import ZSET_KEY, REDIS_PORT, REDIS_SERVER

logger = AppLogger()

class RedisClient:
    
    def __init__(self):
    
        self.redis_client = redis.Redis(host=REDIS_SERVER, port=REDIS_PORT, db=0)
        self.zset_key = ZSET_KEY
        
    def add_job_to_redis_queue(self, job, priority=100):
        try:
            self.redis_client.zadd(self.zset_key, {f"job:{job.id}": priority})
        except redis.RedisError as e:
            logger.error(f"Failed to add Job:{job.id} with priority {priority} to redis: {e}")
            raise
    
    def get_top_job(self):
        try:
            result = self.redis_client.zrange(ZSET_KEY, 0, 0, withscores=True)
            if result: 
                job_id = result[0][0].decode(('utf-8'))
                self.redis_client.zrem(ZSET_KEY, job_id)
                logger.info(f"Redis: get top - {job_id}")
                return job_id.split(":")[1]
            return None
        except redis.RedisError as e:
            logger.error(f"Failed to get top job from redis: {e}")
            raise
     

    def add_to_list(self, data):
        self.redis_client.zadd(self.zset_key, data)
        logger.info(f"Redis: Added - {data}")
