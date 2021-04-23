"""Corpus classes for storing documents to be analyzed"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Iterable, List, Generator, Optional
import datetime
import glob
import os
import shutil

import compress_pickle
import rtoml as toml
import praw
from psaw import PushshiftAPI

import pognlp.constants as constants


class Corpus(ABC):
    """A set of abstract documents to be analyzed. Should be
    automatically persisted to disk whenever it's mutated."""

    def __init__(self, name: str, document_count: int = 0, compiled: bool = False):
        self.name = name
        self.document_count = document_count
        self.directory = os.path.join(constants.corpora_path, name)
        self.toml_path = os.path.join(self.directory, "corpus.toml")
        self.compiled = compiled  # "Compiled" corpora are ready to be analyzed

    @property
    @abstractmethod
    def corpus_type(self) -> str:
        """String representing the type of corpus, used for
        serialization/deserialization"""

    @property
    @abstractmethod
    def document_metadata_fields(self) -> List[str]:
        """Get a list of all metadata field names present on documents in the
        corpus"""

    @abstractmethod
    def write(self) -> None:
        """Serialize self and write to disk"""

    @staticmethod
    @abstractmethod
    def from_dict(corpus_dict: Dict[str, Any]) -> Corpus:
        """Load new corpus from a dict"""

    @staticmethod
    def load(name: str) -> Corpus:
        """Load a corpus from disk given its name"""
        toml_path = os.path.join(constants.corpora_path, name, "corpus.toml")
        with open(toml_path) as toml_file:
            corpus_dict = toml.load(toml_file)

            corpus_by_type = {corpus.corpus_type: corpus for corpus in (RedditCorpus,)}
            corpus_cls = corpus_by_type[corpus_dict["type"]]
            del corpus_dict["type"]
            return corpus_cls.from_dict({"name": name, **corpus_dict})

    @staticmethod
    def ls() -> Iterable[str]:
        """List the names of all corpora saved to disk"""
        return (
            os.path.basename(path)
            for path in glob.iglob(os.path.join(constants.corpora_path, "*"))
        )

    @abstractmethod
    def iterate_documents(self) -> Generator[Dict[str, Any], None, None]:
        """Iterate through the documents stored in the corpus"""

    @abstractmethod
    def compile(
        self, compile_params: Dict[str, Any], progress_cb: Callable[[int], None]
    ) -> None:
        """Perform any work (e.g. downloading) necessary to analyze the
        documents and mark the corpus as ready for analysis"""
        self.compiled = True

    def delete(self) -> None:
        """Delete the corpus from disk"""
        shutil.rmtree(self.directory)


class RedditCorpus(Corpus):
    """A corpus of Reddit comments"""

    corpus_type = "reddit"

    document_metadata_fields = [
        "timestamp",
        "score",
        "comment ID",
        "submission ID",
        "subreddit",
    ]

    def __init__(
        self,
        name: str,
        subreddits: List[str],
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        document_count: int = 0,
        compiled: bool = False,
    ):
        super().__init__(name, document_count=document_count)
        self.subreddits = subreddits
        self.start_time = start_time
        self.end_time = end_time
        self.comments_pickle_path = os.path.join(self.directory, "comments.pickle.gz")

        self.write()

    @staticmethod
    def from_dict(corpus_dict: Dict[str, Any]) -> RedditCorpus:
        return RedditCorpus(
            name=corpus_dict["name"],
            document_count=corpus_dict["document_count"],
            subreddits=corpus_dict["subreddits"],
            start_time=datetime.datetime.fromisoformat(corpus_dict["start_time"]),
            end_time=datetime.datetime.fromisoformat(corpus_dict["end_time"]),
            compiled=corpus_dict["compiled"],
        )

    def write(self) -> None:
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)
        corpus_dict = {
            "type": RedditCorpus.corpus_type,
            "subreddits": self.subreddits,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "document_count": self.document_count,
            "compiled": self.compiled,
        }
        with open(self.toml_path, "w") as toml_file:
            toml.dump(corpus_dict, toml_file)

    def compile(
        self,
        compile_params: Dict[str, Any],
        progress_cb: Optional[Callable[[int], None]] = None,
    ) -> None:
        if self.compiled:
            return

        client_id = compile_params["client_id"]
        client_secret = compile_params["client_secret"]

        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=constants.reddit_user_agent,
        )
        api = PushshiftAPI(reddit)
        comments = []

        start_epoch = int(self.start_time.timestamp())
        end_epoch = int(self.end_time.timestamp())

        progress = 0
        for subreddit in self.subreddits:
            for comment in api.search_comments(
                after=start_epoch, before=end_epoch, subreddit=subreddit
            ):
                comments.append(comment)
                progress += 1
                if progress_cb is not None:
                    progress_cb(progress)

        if not comments:
            raise ValueError("No comments found.")

        self.document_count = len(comments)

        with open(self.comments_pickle_path, "wb") as pickle_file:
            compress_pickle.dump(comments, pickle_file, compression="gzip")

        self.compiled = True
        self.write()

    def iterate_documents(self) -> Generator[Dict[str, Any], None, None]:
        with open(self.comments_pickle_path, "rb") as pickle_file:
            for comment in compress_pickle.load(pickle_file, compression="gzip"):
                yield {
                    "body": comment.body,
                    "timestamp": datetime.datetime.utcfromtimestamp(
                        comment.created_utc
                    ),
                    "score": comment.score,
                    "comment ID": comment.id,
                    "submission ID": comment.submission.id,
                    "subreddit": comment.subreddit.name,
                }
