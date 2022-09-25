from docker_logs import get_logger
from reddit_scraper import get_data
import time
import datetime
from celery_base import app
import celery_base
from celery import group,signature
from embedding_worker import task_submission_embedding
logging = get_logger("scraper_worker")


@app.task(bind=True, name='tasks.submission_fetching', queue="scraping", serializer='pickle')
def task_submission_fetching(self, subreddits):
    for subreddit in subreddits:
        logging.info(f"fetching submissions from subreddit: {subreddit}")
        data = get_data(subreddit)
        posts = []
        for post in data:
            if post.timestamp >= return_time_delta():
                posts.append(post)
        data_count = str(len(posts))
        logging.info(f"Fetched : {data_count}")
        tasks = []
        for post in posts:
            task = signature('task_submission_embedding', args=(post,))
            #logging.info(f"s_em: {s_em.}")
            tasks.append(task)
        group(tasks).apply_async()


def return_time_delta():
    now = datetime.datetime.now(datetime.timezone.utc)
    time_delta = now - datetime.timedelta(seconds=60)
    return time_delta


