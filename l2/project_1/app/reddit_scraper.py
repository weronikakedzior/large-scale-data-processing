import praw
import datetime
import pandas as pd
import json

def define_credentials():
    with open('credentials.json') as json_file:
        data = json.load(json_file)
    reddit = praw.Reddit(
        client_id=data["client_id"],
        client_secret=data["client_secret"],
        user_agent=data["user_agent"]
    )
    return reddit


def get_data(subreddit):
    reddit = define_credentials()
    subreddit = reddit.subreddit(subreddit)
    posts = subreddit.new(limit=10)
    ids = []
    timestamps = []
    comment_num = []
    score = []
    title = []
    for post in posts:
        ids.append(post.id)
        timestamps.append(datetime.datetime.fromtimestamp(post.created_utc, tz=datetime.timezone.utc))
        comment_num.append(post.num_comments)
        score.append(post.score)
        title.append(post.title)
    dict_posts = {
        "id": ids,
        "timestamp": timestamps,
        "comment_num" : comment_num,
        "score": score,
        "title": title
    }
    posts = pd.DataFrame(dict_posts)
    return posts

