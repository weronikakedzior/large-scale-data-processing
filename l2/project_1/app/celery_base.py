from celery import Celery
from docker_logs import get_logger
from reddit_scraper import get_data
from influxdb import InfluxDBClient
import time
import datetime
logging = get_logger("task")

app = Celery()
client = InfluxDBClient(host='influxdb', port=8086, database='database')
#client.drop_database('database')
client.create_database('database')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, task.s('Politics'), name='fetch submission every 60 seconds')


@app.task(bind=True, name='task')  
def task(self, subreddit):
    logging.info(f"fetching submissions from subreddit: {subreddit}")
    start = time.time()
    data = get_data(subreddit)
    end = time.time()
    time_execution = end - start
    data = data[data.timestamp >= return_time_delta()]
    data_count = str(len(data))
    comment_count = data.comment_num.sum()
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
    for index, post in data.iterrows():
        post_score = post.score
        title = post.title
        logging.info(f"Post score {post_score}")
        logging.info(f"Title  {title} len {len(title)}")
        distributions = [
            {
                "measurement": "distributions",
                "time": datetime.datetime.now(),
                "fields": {
                    "post_score": post_score,
                    "title_len": len(title)
                }
            }
        ]
        client.write_points(distributions)
    client.write_points(time_exe)
    client.write_points(counts)



def return_time_delta():
    now = datetime.datetime.now(datetime.timezone.utc)
    time_delta = now - datetime.timedelta(seconds=60)
    return time_delta


