'''Defines different strategies for scheduling jobs'''
from datetime import datetime,timezone
from src.models import Job
from src.logger import AppLogger

logger = AppLogger()

from abc import ABC, abstractmethod
class SchedulerStrategy(ABC):
    '''Abstract method for scheduler strategy'''
    @abstractmethod
    def calculate_score(self, job):
        pass

class SJF_SchedulerStrategy(SchedulerStrategy):
    '''Shortest job first with ageing strategy'''
    def calculate_score(self, job: Job):
        now = datetime.now(timezone.utc) 
        score = now.timestamp()+job.estimated_runtime
        logger.info(f"SJF strategy score: {score}")
        return score
        
class FIFO_SchedulerStrategy(SchedulerStrategy):
    '''First in first out strategy'''
    def calculate_score(self, job: Job):
        now = datetime.now(timezone.utc) 
        return now.timestamp()
