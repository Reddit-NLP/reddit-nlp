from __future__ import annotations

import itertools
import shutil
import glob
import os
from typing import List, Tuple, Iterable
from collections import namedtuple

import rtoml as toml

import pognlp.constants as constants

toml_name = "lexicon.toml"

Word = namedtuple("Word", ["string", "score"])


class DefaultLexicon:
    name = "VADER Default Lexicon"


class Lexicon:
    def __init__(self, name: str, words: List[Tuple[str, float]]):
        self.name = name
        self.words = [Word(*word) for word in words]
        self.directory = os.path.join(constants.lexica_path, name)
        self.toml_path = os.path.join(self.directory, toml_name)
        self.write()

    @staticmethod
    def ls() -> Iterable[str]:
        lexicon_names = (
            os.path.basename(path)
            for path in glob.iglob(os.path.join(constants.lexica_path, "*"))
        )
        return itertools.chain((DefaultLexicon.name,), lexicon_names)

    @staticmethod
    def load(name: str) -> Lexicon | DefaultLexicon:
        if name == DefaultLexicon.name:
            return DefaultLexicon()
        toml_path = os.path.join(constants.lexica_path, name, toml_name)
        with open(toml_path) as toml_file:
            return Lexicon(name=name, **toml.load(toml_file))

    def write(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)
        lexicon_dict = {
            "words": [(word[0], word[1]) for word in self.words],
        }
        with open(self.toml_path, "w") as toml_file:
            toml.dump(lexicon_dict, toml_file)

    def delete(self):
        shutil.rmtree(self.directory)
