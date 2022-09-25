import praw
import json
import datetime
from reddit_submission import RedditSubmission


def define_credentials():
    with open('credentials.json') as json_file:
        data = json.load(json_file)
    reddit = praw.Reddit(
        client_id=data["client_id"],
        client_secret=data["client_secret"],
        user_agent=data["user_agent"]
    )
    return reddit


def get_data(subreddit="all", limit=10):
    reddit = define_credentials()
    subreddit = reddit.subreddit(subreddit)
    posts = subreddit.new(limit=limit)
    submissions = []
    for post in posts:
        author_name = ""
        if post.author.name is not None:
            author_name = post.author.name
        reddit_submission = RedditSubmission(
            url=post.url,
            author_name=author_name,
            subreddit_name=post.subreddit.display_name,
            post_text=post.selftext,
            post_text_em=None,
            number_votes=post.score,
            belongs_to_NSFW=post.over_18,
            num_of_comments=post.num_comments,
            timestamp=datetime.datetime.fromtimestamp(
                                 post.created_utc, tz=datetime.timezone.utc),
            title=post.title,
            text_len=len(post.title + post.selftext))
        submissions.append(reddit_submission)
    return submissions

