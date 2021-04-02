from __future__ import annotations

import shutil
import os
import glob
from typing import List, Generator
import time
import csv
import itertools

import pandas as pd
import numpy as np
import rtoml as toml

from pognlp.analyze import get_analyzer
import pognlp.constants as constants
from pognlp.model.corpus import Corpus
from pognlp.model.lexicon import Lexicon

toml_name = "report.toml"
output_name = "output.tsv"

output_delimiter = "\t"


class Report:
    def __init__(
        self,
        name: str,
        corpus_name: str,
        lexicon_names: List[str],
        complete=False,
    ):
        self.name = name
        self.corpus_name = corpus_name
        self.lexicon_names = lexicon_names
        self.complete = complete
        self.directory = os.path.join(constants.reports_path, name)
        self.toml_path = os.path.join(self.directory, toml_name)
        self.output_path = os.path.join(self.directory, output_name)
        self.write()

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
            return Report(name=name, **toml.load(toml_file))

    def write(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        report_dict = {
            "corpus_name": self.corpus_name,
            "lexicon_names": self.lexicon_names,
            "complete": self.complete,
        }
        with open(self.toml_path, "w") as toml_file:
            toml.dump(report_dict, toml_file)

    def delete(self):
        shutil.rmtree(self.directory)

    def run(self, progress_cb=None):
        corpus = Corpus.load(self.corpus_name)

        n = 0
        with open(self.output_path, "w") as output_file:
            fieldnames = [*corpus.document_metadata_fields]
            analyzers = {}
            for lexicon_name in self.lexicon_names:
                analyzer = get_analyzer(Lexicon.load(lexicon_name))
                analyzers[lexicon_name] = analyzer
                fieldnames.append(f"{lexicon_name} positive")
                fieldnames.append(f"{lexicon_name} neutral")
                fieldnames.append(f"{lexicon_name} negative")
                fieldnames.append(f"{lexicon_name} compound")

            print(fieldnames)

            writer = csv.DictWriter(
                output_file, fieldnames=fieldnames, delimiter=output_delimiter
            )
            writer.writeheader()
            for document in corpus.iterate_documents():
                row_dict = {
                    field: document[field] for field in corpus.document_metadata_fields
                }
                for lexicon_name in self.lexicon_names:
                    scores = analyzers[lexicon_name].polarity_scores(document["body"])
                    print(scores)
                    row_dict[f"{lexicon_name} positive"] = scores["pos"]
                    row_dict[f"{lexicon_name} neutral"] = scores["neu"]
                    row_dict[f"{lexicon_name} negative"] = scores["neg"]
                    row_dict[f"{lexicon_name} compound"] = scores["compound"]

                writer.writerow(row_dict)

                n += 1
                if progress_cb is not None:
                    progress_cb(n)

        self.complete = True
        self.write()

    def get_results(self) -> pd.DataFrame:
        if not self.complete:
            return None

        return pd.read_csv(self.output_path, sep=output_delimiter, parse_dates=True)
