from datetime import datetime,timezone
from models import Job
from logger import AppLogger
logger = AppLogger()

from abc import ABC, abstractmethod
class SchedulerStrategy(ABC):
    @abstractmethod
    def calculate_score(self, job):
        pass

class SJF_SchedulerStrategy(SchedulerStrategy):

    def calculate_score(self, job: Job):
        now = datetime.now(timezone.utc) 
        score = now.timestamp()+job.estimated_runtime
        logger.info(f"SJF strategy score: {score}")
        return score
        
class FIFO_SchedulerStrategy(SchedulerStrategy):

    def calculate_score(self, job: Job):
        now = datetime.now(timezone.utc) 
        return now.timestamp()
