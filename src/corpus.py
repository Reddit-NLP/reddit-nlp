from __future__ import annotations

from abc import ABC, abstractmethod
import datetime
import glob
from typing import Generator
import os
import pickle


import toml
import praw

import constants

class Corpus(ABC):
    def __init__(self, name: str):
        self.name = name
        self.directory = os.path.join(constants.corpora_path, name)
        self.toml_path = os.path.join(self.directory, "corpus.toml")
        self.compiled = False

    @abstractmethod
    def write(self) -> None:
        pass
            
    @staticmethod
    def load(name: str) -> Corpus:
        toml_path = os.path.join(constants.corpora_path, name, "corpus.toml")
        with open(toml_path) as toml_file:
            corpus_dict = toml.load(toml_file, _dict=dict)
            corpus_by_type = {corpus.corpus_type: corpus for corpus in (RedditCorpus,)} # type: ignore
            return corpus_by_type[corpus_dict["type"]].from_dict(corpus_dict)

    @staticmethod
    @abstractmethod
    def from_dict(corpus_dict: dict) -> Corpus:
        pass

    @staticmethod
    def list():
        return [os.path.basename(path) for path in glob.iglob(os.path.join(constants.corpora_path, "*"))]

    @abstractmethod
    def iterate_documents(self) -> Generator[dict, None, None]:
        pass

    def compile(self) -> None:
        self.compiled = True

class RedditCorpus(Corpus):
    corpus_type = "reddit"
    def __init__(self, name: str, subreddits=None, start_time=None, end_time=None):
        super().__init__(name)
        self.subreddits = subreddits or []
        self.start_time = start_time or datetime.datetime.now()
        self.end_time = end_time or datetime.datetime.now()
        self.comments_pickle_path = os.path.join(self.directory, "comments.pickle")
    def write(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)
        corpus_dict = {
            "name": self.name,
            "type": RedditCorpus.corpus_type,
            "subreddits": self.subreddits,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "compiled": self.compiled,
        }
        with open(self.toml_path, "w") as toml_file:
            toml.dump(corpus_dict, toml_file)

    @staticmethod
    def from_dict(corpus_dict: dict):
        corpus = RedditCorpus(
            corpus_dict["name"],
            corpus_dict["subreddits"],
            datetime.datetime.fromisoformat(corpus_dict["start_time"]),
            datetime.datetime.fromisoformat(corpus_dict["end_time"]))
        corpus.compiled = corpus_dict["compiled"]
        return corpus

    def compile(self, client_id: str, client_secret: str):
        reddit = praw.Reddit(
            client_id=os.environ["CLIENT_ID"],
            client_secret=os.environ["CLIENT_SECRET"],
            user_agent="linux:org.reddit-nlp.reddit-nlp:v0.1.0 (by /u/YeetoCalrissian)"
        )
        comments = []
        for subreddit in self.subreddits:
            for submission in reddit.subreddit(subreddit).new(limit=20):
                for comment in submission.comments.list():
                    comments.append(comment)
        with open(self.comments_pickle_path, "wb") as pickle_file:
            pickle.dump(comments, pickle_file)
        self.downloaded = True

    def iterate_documents(self):
        with open(self.comments_pickle_path, "rb") as pickle_file:
            for comment in pickle.load(pickle_file):
                yield {
                    "body": comment.body,
                }

