from celery_base import task
from random import random
from docker_logs import get_logger

logging = get_logger("runner")

#task.delay('worldnews')


#logging.info(f"Task returned: {result}")