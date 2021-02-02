import os
import time
import datetime
from typing import List
from operator import attrgetter
from collections import namedtuple

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import praw

reddit = praw.Reddit(
    client_id=os.environ["CLIENT_ID"],
    client_secret=os.environ["CLIENT_SECRET"],
    user_agent="linux:org.reddit-nlp.reddit-nlp:v0.1.0 (by /u/YeetoCalrissian)"
)

def date_str_to_ts(date_str: str) -> float: 
    """ISO 8601 date string to unix timestamp in seconds"""
    return time.mktime(datetime.datetime.strptime(date_str, "%Y-%m-%d").timetuple())

start_ts = date_str_to_ts("2021-02-01")
end_ts = date_str_to_ts("2021-02-02")


Comment = namedtuple("Comment", ["comment", "body", "score"])
comments: List[Comment] = []

analyser = SentimentIntensityAnalyzer()
for submission in reddit.subreddit("gaming").new(limit=20):
    print(submission.title, submission.created_utc)
    for comment in submission.comments.list():
        body = comment.body.replace("\n", " ")
        score = analyser.polarity_scores(comment.body)
        comments.append(Comment(comment, body, score))

for comment in sorted(comments, key=lambda c: c.score["compound"]):
    print(comment)
