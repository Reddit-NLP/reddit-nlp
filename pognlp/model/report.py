from __future__ import annotations

import os
import glob

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import List, Generator
import numpy as np
import toml

import pognlp.constants as constants
from pognlp.model.corpus import Corpus


class Report:
    def __init__(self, name: str, corpus_name: str, lexicon_names: List[str]):
        self.name = name
        self.corpus_name = corpus_name
        self.lexicon_names = lexicon_names
        self.complete = False
        self.results = (
            {}
        )  # must be TOML-serializable! Maybe switch to pickles if these get big.
        self.directory = os.path.join(constants.reports_path, name)
        self.toml_path = os.path.join(self.directory, "report.toml")

    @staticmethod
    def ls() -> Generator[str, None, None]:
        return (
            os.path.basename(path)
            for path in glob.iglob(os.path.join(constants.reports_path, "*"))
        )

    @staticmethod
    def load(name: str) -> Report:
        toml_path = os.path.join(constants.reports_path, name, "report.toml")
        with open(toml_path) as toml_file:
            return Report(**toml.load(toml_file))

    def write(self):
        if not os.path.exists(constants.reports_path):
            os.makedirs(constants.reports_path, exist_ok=True)
        report_dict = {
            "name": self.name,
            "corpus_name": self.corpus_name,
            "lexicon_names": self.lexicon_names,
            "complete": self.complete,
            "results": self.results,
        }
        with open(self.toml_path, "w") as toml_file:
            toml.dump(report_dict, toml_file)

    def run(self):
        corpus = Corpus.load(self.corpus_name)

        n = 0
        pos = []
        neu = []
        neg = []
        compound = []

        analyzer = SentimentIntensityAnalyzer()

        for document in corpus.iterate_documents():
            n += 1
            print(document["body"])
            scores = analyzer.polarity_scores(document["body"])
            pos.append(scores["pos"])
            neu.append(scores["neu"])
            neg.append(scores["neg"])
            compound.append(scores["compound"])

        # TODO for now, print to stdout. later, store results in the class and
        # call a callback to update the UI

        pos = np.array(pos)
        neu = np.array(neu)
        neg = np.array(neg)
        compound = np.array(compound)

        pos_mean = np.mean(pos)
        neu_mean = np.mean(neu)
        neg_mean = np.mean(neg)
        compound_mean = np.mean(compound)

        pos_std = np.std(pos)
        neu_std = np.std(neu)
        neg_std = np.std(neg)
        compound_std = np.std(compound)

        print(
            "Analyzing corpus using VADER (Valence Aware Dictionary and sEntiment Reasoner)"
        )

        print(f"{pos_mean=} {neu_mean=} {neg_mean=}")
        print(f"{pos_std=} {neu_std=} {neg_std=}")
