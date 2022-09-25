from docker_logs import get_logger
from pymagnitude import Magnitude
from celery_base import app
import numpy as np
from celery import signature
from database_worker import task_submission_save
from reddit_submission import RedditSubmission
logging = get_logger("embedding_worker")


@app.task(bind=True, name='task_submission_embedding', queue="embedding", serializer='pickle')
def task_submission_embedding(self, post: RedditSubmission):
    logging.info(f"Start embedding calculating")
    text = post.title + " " + post.post_text
    vectors = Magnitude("embedding/GoogleNews.magnitude")
    embeddings = vectors.query(text.split())
    embedding = np.mean(embeddings, axis=0)
    post.post_text_em = embedding.tolist()
    #logging.info(f"Text em: {post.text_em}")
    signature('tasks.task_submission_save', args=(post,)).apply_async()
    #task_submission_save.s(post).apply_async()
    return post
