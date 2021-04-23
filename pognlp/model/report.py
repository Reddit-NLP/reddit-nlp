"""Report class"""

from __future__ import annotations

import shutil
import os
import glob
from typing import Callable, Dict, Iterable, List, Optional
import csv
from collections import defaultdict, Counter

import spacy
import pandas as pd
import rtoml as toml
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from pognlp.analyze import get_analyzer
import pognlp.constants as constants
from pognlp.model.corpus import Corpus
from pognlp.model.lexicon import DefaultLexicon, Lexicon

TOML_NAME = "report.toml"
OUTPUT_NAME = "output.tsv"
FREQUENCY_NAME = "frequency.tsv"

DELIMITER = "\t"


class Report:
    """A pairing of a corpus and a set of lexica used to analyze that corpus"""

    def __init__(
        self,
        name: str,
        corpus_name: str,
        lexicon_names: List[str],
        complete: bool = False,
    ):
        self.name = name
        self.corpus_name = corpus_name
        self.lexicon_names = lexicon_names
        self.complete = complete
        self.run_in_progress = False
        self.directory = os.path.join(constants.reports_path, name)
        self.toml_path = os.path.join(self.directory, TOML_NAME)
        self.output_path = os.path.join(self.directory, OUTPUT_NAME)
        self.frequency_path = os.path.join(self.directory, FREQUENCY_NAME)
        self.write()

    @staticmethod
    def ls() -> Iterable[str]:
        """List the names of all reports saved to disk"""
        return (
            os.path.basename(path)
            for path in glob.iglob(os.path.join(constants.reports_path, "*"))
        )

    @staticmethod
    def load(name: str) -> Report:
        """Load a report from disk given its name"""
        toml_path = os.path.join(constants.reports_path, name, TOML_NAME)
        with open(toml_path) as toml_file:
            return Report(name=name, **toml.load(toml_file))

    def write(self) -> None:
        """Serialize and write the report to disk"""
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        report_dict = {
            "corpus_name": self.corpus_name,
            "lexicon_names": self.lexicon_names,
            "complete": self.complete,
        }
        with open(self.toml_path, "w") as toml_file:
            toml.dump(report_dict, toml_file)

    def delete(self) -> None:
        """Delete a report"""
        shutil.rmtree(self.directory)

    def run(
        self,
        progress_cb: Optional[Callable[[int], None]] = None,
        include_body: bool = False,
    ) -> None:
        """Run the report

        Where the magic happens. For each lexicon, get sentiment scores for
        each document in the corpus and count the frequency of each word in the
        lexicon. Store results in TSV files on disk in the report's directory.
        Optionally call `progress_cb` when any progress is made with an
        incrementing value (unfortunately, a true "determinate" progress value
        from 0 to 1 is not available). Optionally include the body of each
        document in the report's output."""

        self.run_in_progress = False

        # Reset `complete` status in case we're re-running the report
        self.complete = False

        corpus = Corpus.load(self.corpus_name)

        progress = 0

        output_fieldnames = [*corpus.document_metadata_fields]
        analyzers: Dict[str, SentimentIntensityAnalyzer] = {}
        if include_body:
            output_fieldnames.insert(0, "body")

        frequencies = Counter[str]()
        frequency_fieldnames = [
            "lemmatized word",
            "lexicon name",
            "frequency per 10,000",
        ]

        # To get a meaningful frequency count, lemmatize the words before
        # counting them. Lemmatization reduces a word to its base form. See
        # https://en.wikipedia.org/wiki/Lemmatisation.

        # Keep track of the set of lexica that each lemma belongs to. Lambda is
        # necessary here since defaultdict expects a factory function, and
        # anyways we need a separate instance of set for each key
        # pylint: disable=unnecessary-lambda
        lexicon_lemmas = defaultdict(lambda: set())

        # the set of all lemmas
        all_lexicon_lemmas = set()

        # the total word count in the corpus for relative frequency counts
        total_token_count = 0

        # Use Spacy for lemmatization
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
                    progress += 1
                    if progress_cb is not None:
                        progress_cb(progress)
                    lemmatized = " ".join(
                        token.lemma_ for token in nlp(word.string)
                    ).lower()
                    lexicon_lemmas[lexicon_name].add(lemmatized)
                    all_lexicon_lemmas.add(lemmatized)

        # Open both output TSV files for writing
        with open(self.output_path, "w") as output_file, open(
            self.frequency_path, "w"
        ) as frequency_file:
            output_writer = csv.DictWriter(
                output_file, fieldnames=output_fieldnames, delimiter=DELIMITER
            )
            output_writer.writeheader()

            frequency_writer = csv.DictWriter(
                frequency_file, fieldnames=frequency_fieldnames, delimiter=DELIMITER
            )
            frequency_writer.writeheader()

            for index, document in enumerate(corpus.iterate_documents()):
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
                    sanitized_body = (
                        document["body"].replace("\n", " ").replace("\t", " ")
                    )
                    output_row_dict["body"] = sanitized_body
                for lexicon_name in self.lexicon_names:
                    scores = analyzers[lexicon_name].polarity_scores(document["body"])
                    output_row_dict[f"{lexicon_name} positive"] = scores["pos"]
                    output_row_dict[f"{lexicon_name} neutral"] = scores["neu"]
                    output_row_dict[f"{lexicon_name} negative"] = scores["neg"]
                    output_row_dict[f"{lexicon_name} compound"] = scores["compound"]

                output_writer.writerow(output_row_dict)

                if progress_cb is not None:
                    progress_cb(100 * (index // corpus.document_count))

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
        """Return a dataframe of the report results"""
        if not self.complete:
            return None

        return pd.read_csv(self.output_path, sep=DELIMITER, parse_dates=True)

    def get_frequencies(self) -> pd.DataFrame:
        """Return a dataframe of the word frequencies"""
        if not self.complete:
            return None
        return pd.read_csv(self.frequency_path, sep=DELIMITER)
