from __future__ import annotations

import shutil
import os
import glob
from typing import List, Generator
import time
import csv
from collections import defaultdict, Counter
import itertools

import spacy
import pandas as pd
import numpy as np
import rtoml as toml

from pognlp.analyze import get_analyzer
import pognlp.constants as constants
from pognlp.model.corpus import Corpus
from pognlp.model.lexicon import DefaultLexicon, Lexicon

toml_name = "report.toml"
output_name = "output.tsv"
frequency_name = "frequency.tsv"

delimiter = "\t"


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
        self.frequency_path = os.path.join(self.directory, frequency_name)
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

    def run(self, progress_cb=None, include_body=False):
        corpus = Corpus.load(self.corpus_name)

        n = 0

        output_fieldnames = [*corpus.document_metadata_fields]
        analyzers = {}
        if include_body:
            output_fieldnames.insert(0, "body")

        frequencies = Counter()
        frequency_fieldnames = [
            "lemmatized word",
            "lexicon name",
            "frequency per 10,000",
        ]
        lexicon_lemmas = defaultdict(lambda: [])
        all_lexicon_lemmas = set()
        total_token_count = 0

        nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

        for lexicon_name in self.lexicon_names:
            lexicon = Lexicon.load(lexicon_name)
            analyzer = get_analyzer(lexicon)
            analyzers[lexicon_name] = analyzer
            output_fieldnames.append(f"{lexicon_name} positive")
            output_fieldnames.append(f"{lexicon_name} neutral")
            output_fieldnames.append(f"{lexicon_name} negative")
            output_fieldnames.append(f"{lexicon_name} compound")
            if not isinstance(lexicon, DefaultLexicon):
                for word in lexicon.words:
                    lemmatized = " ".join(
                        token.lemma_ for token in nlp(word.string)
                    ).lower()
                    lexicon_lemmas[lexicon_name].append(lemmatized)
                    all_lexicon_lemmas.add(lemmatized)

        with open(self.output_path, "w") as output_file, open(
            self.frequency_path, "w"
        ) as frequency_file:
            output_writer = csv.DictWriter(
                output_file, fieldnames=output_fieldnames, delimiter=delimiter
            )
            output_writer.writeheader()

            frequency_writer = csv.DictWriter(
                frequency_file, fieldnames=frequency_fieldnames, delimiter=delimiter
            )
            frequency_writer.writeheader()

            for document in corpus.iterate_documents():
                doc = nlp(document["body"])
                for token in doc:
                    total_token_count += 1
                    lemma = token.lemma_.lower()
                    if lemma in all_lexicon_lemmas:
                        frequencies[lemma] += 1

                output_row_dict = {
                    field: document[field] for field in corpus.document_metadata_fields
                }
                if include_body:
                    sanitized_body = document["body"].replace("\n", " ").replace("\t", " ")
                    output_row_dict["body"] = sanitized_body
                for lexicon_name in self.lexicon_names:
                    scores = analyzers[lexicon_name].polarity_scores(document["body"])
                    output_row_dict[f"{lexicon_name} positive"] = scores["pos"]
                    output_row_dict[f"{lexicon_name} neutral"] = scores["neu"]
                    output_row_dict[f"{lexicon_name} negative"] = scores["neg"]
                    output_row_dict[f"{lexicon_name} compound"] = scores["compound"]

                output_writer.writerow(output_row_dict)

                n += 1
                if progress_cb is not None:
                    progress_cb(n)

            for lexicon_name in self.lexicon_names:
                for lemma in lexicon_lemmas[lexicon_name]:
                    try:
                        relative_frequency = (
                            frequencies[lemma] * 10000 / total_token_count
                        )
                    except ZeroDivisionError:
                        relative_frequency = 0
                    frequency_writer.writerow(
                        {
                            "lemmatized word": lemma,
                            "lexicon name": lexicon_name,
                            "frequency per 10,000": relative_frequency,
                        }
                    )

        self.complete = True
        self.write()

    def get_results(self) -> pd.DataFrame:
        if not self.complete:
            return None

        return pd.read_csv(self.output_path, sep=delimiter, parse_dates=True)

    def get_frequencies(self) -> pd.DataFrame:
        if not self.complete:
            return None
        return pd.read_csv(self.frequency_path, sep=delimiter)
