from __future__ import annotations

import shutil
import os
import glob
from typing import List, Generator

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import toml

import pognlp.constants as constants
from pognlp.model.corpus import Corpus

toml_name = "report.toml"


class Report:
    def __init__(
        self,
        name: str,
        corpus_name: str,
        lexicon_names: List[str],
        complete=False,
        results=None,
    ):
        self.name = name
        self.corpus_name = corpus_name
        self.lexicon_names = lexicon_names
        self.complete = complete
        self.results = results or {}
        self.directory = os.path.join(constants.reports_path, name)
        self.toml_path = os.path.join(self.directory, toml_name)

    @staticmethod
    def ls() -> Generator[str, None, None]:
        return (
            os.path.basename(path)
            for path in glob.iglob(os.path.join(constants.reports_path, "*"))
        )

    @staticmethod
    def load(name: str) -> Report:
        toml_path = os.path.join(constants.reports_path, name, toml_name)
        with open(toml_path) as toml_file:
            return Report(**toml.load(toml_file))

    def write(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        report_dict = {
            "name": self.name,
            "corpus_name": self.corpus_name,
            "lexicon_names": self.lexicon_names,
            "complete": self.complete,
            "results": self.results,
        }
        with open(self.toml_path, "w") as toml_file:
            toml.dump(report_dict, toml_file)

    def delete(self):
        shutil.rmtree(self.directory)

    def run(self, progress_cb=None):
        corpus = Corpus.load(self.corpus_name)

        n = 0
        pos = []
        neu = []
        neg = []
        compound = []

        analyzer = SentimentIntensityAnalyzer()

        for document in corpus.iterate_documents():
            print(document["body"])
            scores = analyzer.polarity_scores(document["body"])
            pos.append(scores["pos"])
            neu.append(scores["neu"])
            neg.append(scores["neg"])
            compound.append(scores["compound"])
            n += 1
            progress_cb(n)

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

        self.results[
            "text"
        ] = "Analyzing corpus using VADER (Valence Aware Dictionary and sEntiment Reasoner)\n"

        self.results["text"] += f"{pos_mean=} {neu_mean=} {neg_mean=}\n"
        self.results["text"] += f"{pos_std=} {neu_std=} {neg_std=}\n"

        self.complete = True
        self.write()
