from celery import shared_task,Task
from celery.utils.log import get_task_logger

class CustomTaskBase(Task):
    autoretry_for = (ConnectionError,TimeoutError,ConnectionResetError)
    retry_kwargs = {'max_retries': 3}
    retry_backoff = True
    logger = get_task_logger(__name__)
    
    def before_start(self, task_id, args, kwargs):
        self.logger.info(f"[PENDING] {self.name} {task_id} started. Variables: {args}")
        super().before_start(task_id, args, kwargs)
    
    def on_success(self, retval, task_id, args, kwargs):
        self.logger.info(f"[SUCCESS]{self.name} {task_id} completed successfully")
        super().on_success(retval, task_id, args, kwargs)
        
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.logger.info(f"[FAILURE]{self.name} {task_id} failed")
        return super().on_failure(exc, task_id, args, kwargs, einfo)
    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        self.logger.info(f"[COMPLETION] {self.name} {task_id} ended with status : {status}")
        return super().after_return(status, retval, task_id, args, kwargs, einfo)
    
    def get_logger(self):
        return self.logger

    

@shared_task(base=CustomTaskBase,ignore_result = False)
def add_together(a:int, b:int) -> int:
    return a+b

@shared_task(base=CustomTaskBase,ignore_result = False)
def mul(a:int, b:int) -> int:
    return a*b
  
@shared_task(base=CustomTaskBase,ignore_result = False)
def xsum(*args):
    return sum(args)

