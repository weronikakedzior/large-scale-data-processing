from docker_logs import get_logger
from pymongo import MongoClient
from celery_base import app
from reddit_submission import RedditSubmission


logging = get_logger("database_worker")


@app.task(bind=True, name='tasks.task_submission_save', queue="database", serializer='pickle')
def task_submission_save(self, post: RedditSubmission):
    logging.info(f"Start saving submission")
    client = MongoClient('mongodb://user:passwd@mongodb:27017/')
    db = client.reddit_database
    collection = db['post-collection']
    post_dict = change_to_dict(self, post)
    logging.info(f"Subreddit: {post.subreddit_name}")
    post_id = collection.insert_one(post_dict).inserted_id

    logging.info(f"Inserted: {post_id}")
    return post


def change_to_dict(self, post: RedditSubmission):
    return {"url": post.url,
            "author_name": post.author_name,
            "subreddit_name": post.subreddit_name,
            "post_text": post.post_text,
            "post_text_em": post.post_text_em,
            "number_votes": post.number_votes,
            "belongs_to_NSFW": post.belongs_to_NSFW,
            "num_of_comments": post.num_of_comments,
            "title": post.title,
            "text_len": post.text_len
           }




