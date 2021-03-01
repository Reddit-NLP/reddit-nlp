from __future__ import annotations

import shutil
import glob
import os
from typing import List, Tuple, Generator
from collections import namedtuple

import rtoml as toml

import pognlp.constants as constants

toml_name = "lexicon.toml"

Word = namedtuple("Word", ["string", "score"])


class Lexicon:
    def __init__(self, name: str, words: List[Tuple[str, float]]):
        self.name = name
        self.words = [Word(*word) for word in words]
        self.directory = os.path.join(constants.lexica_path, name)
        self.toml_path = os.path.join(self.directory, toml_name)

    @staticmethod
    def ls() -> Generator[str, None, None]:
        return (
            os.path.basename(path)
            for path in glob.iglob(os.path.join(constants.lexica_path, "*"))
        )

    @staticmethod
    def load(name: str) -> Lexicon:
        toml_path = os.path.join(constants.lexica_path, name, toml_name)
        with open(toml_path) as toml_file:
            return Lexicon(**toml.load(toml_file))

    def write(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)
        report_dict = {
            "name": self.name,
            "words": [(string, score) for word in self.words],
        }
        with open(self.toml_path, "w") as toml_file:
            toml.dump(lexicon_dict, toml_file)

    def delete(self):
        shutil.rmtree(self.directory)
