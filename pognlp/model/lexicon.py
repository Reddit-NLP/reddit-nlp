"""Lexica to use for analysis"""

from __future__ import annotations

import itertools
import shutil
import glob
import os
from typing import List, Iterable, Tuple, Union
from collections import namedtuple

import rtoml as toml

import pognlp.constants as constants

TOML_NAME = "lexicon.toml"

Word = namedtuple("Word", ["string", "score"])


# pylint: disable=too-few-public-methods
class DefaultLexicon:
    """Stub class to represent the VADER default lexicon"""

    name = "VADER Default Lexicon"


class Lexicon:
    """A list of words paired with corresponding sentiment scores.
    Automatically persisted to disk."""

    def __init__(self, name: str, words: List[Tuple[str, float]]):
        self.name = name
        self.words = [Word(*word) for word in words]
        self.directory = os.path.join(constants.lexica_path, name)
        self.toml_path = os.path.join(self.directory, TOML_NAME)
        self.write()

    @staticmethod
    def ls() -> Iterable[str]:
        """List the names of all lexica saved to disk"""
        lexicon_names = (
            os.path.basename(path)
            for path in glob.iglob(os.path.join(constants.lexica_path, "*"))
        )
        return itertools.chain((DefaultLexicon.name,), lexicon_names)

    @staticmethod
    def load(name: str) -> Union[Lexicon, DefaultLexicon]:
        """Load a lexicon from disk given its name"""
        if name == DefaultLexicon.name:
            return DefaultLexicon()
        toml_path = os.path.join(constants.lexica_path, name, TOML_NAME)
        with open(toml_path, encoding="utf-8") as toml_file:
            return Lexicon(name=name, **toml.load(toml_file))

    def write(self) -> None:
        """Serialize and write the lexicon to disk as a TOML file"""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)
        lexicon_dict = {
            "words": [(word[0], word[1]) for word in self.words],
        }
        with open(self.toml_path, "w", encoding="utf-8") as toml_file:
            toml.dump(lexicon_dict, toml_file)

    def delete(self) -> None:
        """Delete the lexicon"""
        shutil.rmtree(self.directory)
