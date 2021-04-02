from __future__ import annotations

from abc import ABC, abstractmethod
import datetime
import glob
from typing import List, Generator
import os
import shutil
import pickle


import rtoml as toml
import praw
from psaw import PushshiftAPI

import pognlp.constants as constants


class Corpus(ABC):
    def __init__(self, name: str, compiled=False):
        self.name = name
        self.directory = os.path.join(constants.corpora_path, name)
        self.toml_path = os.path.join(self.directory, "corpus.toml")
        self.compiled = False

    @property
    @abstractmethod
    def document_metadata_fields(self) -> List[str]:
        pass

    @abstractmethod
    def write(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def from_dict(corpus_dict: dict) -> Corpus:
        pass

    @staticmethod
    def load(name: str) -> Corpus:
        toml_path = os.path.join(constants.corpora_path, name, "corpus.toml")
        with open(toml_path) as toml_file:
            corpus_dict = toml.load(toml_file)

            corpus_by_type = {corpus.corpus_type: corpus for corpus in (RedditCorpus,)}  # type: ignore
            corpus_cls = corpus_by_type[corpus_dict["type"]]
            del corpus_dict["type"]
            return corpus_cls.from_dict({"name": name, **corpus_dict})

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

    def delete(self):
        shutil.rmtree(self.directory)


class RedditCorpus(Corpus):
    corpus_type = "reddit"

    document_metadata_fields = ["timestamp", "score"]

    def __init__(
        self, name: str, compiled=False, subreddits=None, start_time=None, end_time=None
    ):
        super().__init__(name)
        self.subreddits = subreddits or []
        self.start_time = start_time
        self.end_time = end_time
        self.comments_pickle_path = os.path.join(self.directory, "comments.pickle")

        self.write()

    @staticmethod
    def from_dict(corpus_dict: dict):
        return RedditCorpus(
            name=corpus_dict["name"],
            start_time=datetime.datetime.fromisoformat(corpus_dict["start_time"]),
            end_time=datetime.datetime.fromisoformat(corpus_dict["end_time"]),
            subreddits=corpus_dict["subreddits"],
            compiled=corpus_dict["compiled"],
        )

    def write(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)
        corpus_dict = {
            "type": RedditCorpus.corpus_type,
            "subreddits": self.subreddits,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "compiled": self.compiled,
        }
        with open(self.toml_path, "w") as toml_file:
            toml.dump(corpus_dict, toml_file)

    def compile(self, compile_params, progress_cb=None):
        if self.compiled:
            return

        client_id = compile_params["client_id"]
        client_secret = compile_params["client_secret"]

        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="linux:org.reddit-nlp.reddit-nlp:v0.1.0 (by /u/YeetoCalrissian)",
        )
        api = PushshiftAPI(reddit)
        comments = []

        start_epoch = int(self.start_time.timestamp())
        end_epoch = int(self.end_time.timestamp())

        n = 0
        for subreddit in self.subreddits:
            print(subreddit, start_epoch, end_epoch)
            for comment in api.search_comments(
                after=start_epoch, before=end_epoch, subreddit=subreddit
            ):
                comments.append(comment)
                n += 1
                if progress_cb is not None:
                    progress_cb(n)

        with open(self.comments_pickle_path, "wb") as pickle_file:
            pickle.dump(comments, pickle_file)

        self.compiled = True
        self.write()

    def iterate_documents(self):
        with open(self.comments_pickle_path, "rb") as pickle_file:
            for comment in pickle.load(pickle_file):
                yield {
                    "body": comment.body,
                    "score": comment.score,
                    "timestamp": datetime.datetime.utcfromtimestamp(
                        comment.created_utc
                    ),
                }
