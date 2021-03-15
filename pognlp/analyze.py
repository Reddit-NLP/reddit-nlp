from collections import namedtuple
import codecs
import tempfile

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

AnalysisResult = namedtuple("AnalysisResult", ["document", "score"])


class CustomSentimentIntensityAnalyzer(SentimentIntensityAnalyzer):
    """
    Give a sentiment intensity score to sentences.
    """

    def __init__(self, lexicon_file_contents):
        self.lexicon_full_filepath = lexicon_file_contents
        self.lexicon = self.make_lex_dict()

        self.emojis = {}


def get_lexicon_file_lines(lexicon):
    for word in lexicon.words:
        string = word.string.replace("\t", " ")  # sanitize for tabs
        yield f"{string}\t{word.score}"


def get_analyzer(lexicon=None):
    if lexicon is None:
        return SentimentIntensityAnalyzer()
    lexicon_file_contents = "\n".join(get_lexicon_file_lines(lexicon))
    return CustomSentimentIntensityAnalyzer(lexicon_file_contents)
