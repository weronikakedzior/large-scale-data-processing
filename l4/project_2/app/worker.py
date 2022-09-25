from celery_base import *
from scraper_worker import task_submission_fetching

subreddits = ["AskReddit", "politics", "funny", "news", "memes"]


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, task_submission_fetching.s(subreddits), name='fetch - embed - save submission every 60 seconds')
