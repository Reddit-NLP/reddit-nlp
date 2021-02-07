from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import List
import numpy as np

from corpus import Corpus

class Report:
    def __init__(self, corpus_name: str, lexicon_names: List[str]):
        self.corpus_name = corpus_name
        self.lexicon_names = lexicon_names

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
            scores = analyzer.polarity_scores(document["body"])
            pos.append(scores["pos"])
            neu.append(scores["neu"])
            neg.append(scores["neg"])
            compound.append(scores["compound"])

        # TODO for now, print to stdout. later, store results in the class and call a callback to update the UI

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

        print(f"{pos_mean=} {neu_mean=} {neg_mean=}")
        print(f"{pos_std=} {neu_std=} {neg_std=}")
