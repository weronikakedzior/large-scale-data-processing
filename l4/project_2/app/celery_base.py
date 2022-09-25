from celery import Celery
from docker_logs import get_logger
logging = get_logger("task")

app = Celery()
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['pickle']
