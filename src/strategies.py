from datetime import datetime,timezone
from models import Job

from abc import ABC, abstractmethod
class SchedulerStrategy(ABC):
    @abstractmethod
    def calculate_score(self, job):
        pass

class SJF_SchedulerStrategy(SchedulerStrategy):

    def calculate_score(self, job: Job):
        now = datetime.now(timezone.utc) 
        return now.timestamp()+job.estimated_runtime
        
class FIFO_SchedulerStrategy(SchedulerStrategy):

    def calculate_score(self, job: Job):
        now = datetime.now(timezone.utc) 
        return now.timestamp()
