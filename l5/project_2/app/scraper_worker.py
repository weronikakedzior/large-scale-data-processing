import os

from influxdb import InfluxDBClient

from docker_logs import get_logger
from reddit_scraper import get_data
import time
import datetime
from celery_base import app
import celery_base
from celery import group, signature
from embedding_worker import task_submission_embedding
logging = get_logger("scraper_worker")
client = InfluxDBClient(host=os.environ['INFLUXDB_HOST'], port=os.environ['INFLUXDB_PORT'],
                        username=os.environ['INFLUXDB_USERNAME'], password=os.environ['INFLUXDB_PASS'],
                        database='my_database')
client.create_database('database')


@app.task(bind=True, name='tasks.submission_fetching', queue="scraping", serializer='pickle')
def task_submission_fetching(self, subreddits):
    for subreddit in subreddits:
        logging.info(f"fetching submissions from subreddit: {subreddit}")
        start = time.time()
        data = get_data(subreddit)
        end = time.time()
        time_execution = end - start
        comment_count = 0
        posts = []
        for post in data:
            if post.timestamp >= return_time_delta():
                posts.append(post)
                comment_count += post.num_of_comments
        data_count = str(len(posts))
        logging.info(f"Fetched : {data_count}")
        time_exe = [
            {
                "measurement": "time_exe",
                "time": datetime.datetime.now(),
                "fields": {
                    "duration": time_execution
                }
            }
        ]
        counts = [
            {
                "measurement": "counts",
                "time": datetime.datetime.now(),
                "fields": {
                    "post_count": len(data),
                    "comment_count": comment_count
                }
            }
        ]
        tasks = []

        for post in posts:
            distributions = [
                {
                    "measurement": "distributions",
                    "time": datetime.datetime.now(),
                    "fields": {
                        "post_score": post.number_votes,
                        "title_len": len(post.title)
                    }
                }
            ]
            client.write_points(distributions)
            task = signature('task_submission_embedding', args=(post,))
            #logging.info(f"s_em: {s_em.}")
            tasks.append(task)
        client.write_points(time_exe)
        client.write_points(counts)
        group(tasks).apply_async()


def return_time_delta():
    now = datetime.datetime.now(datetime.timezone.utc)
    time_delta = now - datetime.timedelta(seconds=60)
    return time_delta


