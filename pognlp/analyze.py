"""Set up sentiment intensity analysis using VADER"""

from collections import namedtuple
from typing import Dict, Generator, Union

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from pognlp.vader_lexicon import VADER_LEXICON
from pognlp.model.lexicon import DefaultLexicon, Lexicon

AnalysisResult = namedtuple("AnalysisResult", ["document", "score"])


# This class is just to patch VADER so we can pass our own lexicon without
# creating temporary files.
# pylint: disable=too-few-public-methods
class CustomSentimentIntensityAnalyzer(SentimentIntensityAnalyzer):
    """
    Sentiment analyzer with a custom lexicon. `lexicon_file_contents` contains
    the text of a TSV file in the VADER format, i.e:

    word1\tscore1
    word2\tscore2
    ...

    """

    def __init__(self, lexicon_file_contents: str):
        self.lexicon_full_filepath = lexicon_file_contents
        self.lexicon = self.make_lex_dict()

        self.emojis: Dict[str, str] = {}


def get_lexicon_file_lines(lexicon: Lexicon) -> Generator[str, None, None]:
    """
    Iterate over words in a lexicon and yield word, sentiment score pairs as lines in a TSV
    """
    for word in lexicon.words:
        string = word.string.replace("\t", " ").replace(
            "\n", " "
        )  # sanitize for tabs and newlines in the word
        yield f"{string}\t{word.score}"


def get_analyzer(lexicon: Union[Lexicon, DefaultLexicon]) -> SentimentIntensityAnalyzer:
    """Given a lexicon, return a VADER SentimentIntensityAnalyzer instance that
    analyzes documents using that lexicon"""

    if isinstance(lexicon, DefaultLexicon):
        return CustomSentimentIntensityAnalyzer(VADER_LEXICON)

    # turn the custom lexicon into a TSV and pass it to VADER
    lexicon_file_contents = "\n".join(get_lexicon_file_lines(lexicon))
    return CustomSentimentIntensityAnalyzer(lexicon_file_contents)
