from __future__ import annotations

from abc import ABC, abstractmethod
import datetime
import glob
from typing import Generator
import os
import pickle


import toml
import praw

import pognlp.constants as constants


class Corpus(ABC):
    def __init__(self, name: str, compiled=False):
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

            corpus_by_type = {corpus.corpus_type: corpus for corpus in (RedditCorpus,)}  # type: ignore
            corpus_cls = corpus_by_type[corpus_dict["type"]]
            del corpus_dict["type"]
            return corpus_cls(**corpus_dict)

    @staticmethod
    def ls():
        return [
            os.path.basename(path)
            for path in glob.iglob(os.path.join(constants.corpora_path, "*"))
        ]

    @abstractmethod
    def iterate_documents(self) -> Generator[dict, None, None]:
        pass

    def compile(self, compile_params) -> None:
        self.compiled = True


class RedditCorpus(Corpus):
    corpus_type = "reddit"

    def __init__(
        self, name: str, compiled=False, subreddits=None, start_time=None, end_time=None
    ):
        super().__init__(name)
        self.subreddits = subreddits or []
        self.start_time = (
            datetime.datetime.fromisoformat(start_time) or datetime.datetime.now()
        )
        self.end_time = (
            datetime.datetime.fromisoformat(end_time) or datetime.datetime.now()
        )
        self.comments_pickle_path = os.path.join(self.directory, "comments.pickle")
        self.write()

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

    def compile(self, compile_params):
        # client_id = compile_params["client_id"]
        # client_secret = compile_params["client_secret"]
        reddit = praw.Reddit(
            client_id=os.environ["CLIENT_ID"],
            client_secret=os.environ["CLIENT_SECRET"],
            user_agent="linux:org.reddit-nlp.reddit-nlp:v0.1.0 (by /u/YeetoCalrissian)",
        )
        comments = []
        for subreddit in self.subreddits:
            for submission in reddit.subreddit(subreddit).new(limit=20):
                for comment in submission.comments.list():
                    comments.append(comment)
        with open(self.comments_pickle_path, "wb") as pickle_file:
            pickle.dump(comments, pickle_file)
        self.compiled = True
        self.write()

    def iterate_documents(self):
        with open(self.comments_pickle_path, "rb") as pickle_file:
            for comment in pickle.load(pickle_file):
                yield {
                    "body": comment.body,
                }
