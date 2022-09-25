class RedditSubmission:
    def __init__(self, url, author_name, subreddit_name,
                 post_text, post_text_em, number_votes, belongs_to_NSFW,
                 num_of_comments, timestamp, title, text_len):
        self.url = url
        self.author_name = author_name
        self.subreddit_name = subreddit_name
        self.post_text = post_text
        self.post_text_em = post_text_em
        self.number_votes = number_votes
        self.belongs_to_NSFW = belongs_to_NSFW
        self.num_of_comments = num_of_comments
        self.timestamp = timestamp
        self.title = title
        self.text_len = text_len

