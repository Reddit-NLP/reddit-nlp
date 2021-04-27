# PogNLP

## Introduction

PogNLP was developed to help CDC researchers identify risk and protective factors of youth violence in online communities, with a focus on gaming-related communities. It can download comment data from Reddit and analyze them using VADER, a dictionary-based sentiment analyzer. The lexicon used by VADER can be changed in order to target certain types of violence or refine the search to identify violence more effectively. The results of the analysis can be exported as a TSV file and processed using another application, like Excel.

## Release Notes

### PogNLP v1.0.0
New Features

- Allows comment data to be downloaded from Reddit
- Allows creation of custom lexica (dictionaries) to be created for the sentiment analysis algorithm
- Can run the sentiment analysis algorithm on downloaded data using created lexica and export the results
- Has a progress bar to indicate progress of download or report creation

Bug Fixes

- Added error messages when the download or report is unsuccessful
- Fixed issue where two reports could not be run simultaneously
- Fixed issues where you could not create multiple corpora without restarting the app

Known Bugs

- If the supplied Reddit API credentials are invalid, the application reports that no comments were found instead of showing an appropriate error.

## Install Guide

Downloads for GNU/Linux and Windows are available for download in the [Releases section](https://github.com/Reddit-NLP/reddit-nlp/releases). These executables do not require Python to be installed and should work on any recent system.


## User Guide

1. Obtain a Reddit API client token and secret according to these instructions: [https://github.com/reddit-archive/reddit/wiki/OAuth2#getting-started](https://github.com/reddit-archive/reddit/wiki/OAuth2#getting-started)

2. Download the application from the [Releases section](https://github.com/Reddit-NLP/reddit-nlp/releases) and run it. Your operating system may warn that the executable is unsigned or untrustworthy.

3. Start by downloading a new corpus of data from Reddit, either by clicking the "Download New Data" button on the home screen or by clicking the "New Reddit Corpus" button on the "Corpora" screen. Enter the start and end dates for your search in the fields provided. A format like "April 4 2021" works best, but it should be able to understand most date and time formats. Inserting specific hours of the day to indicate time is optional and up to the user's discretion. Next, enter the list of subreddit names you'd like to search (without "/r/", just the names), one reddit thread per line. Enter your Reddit API credentials from earlier. Finally, enter a name for your corpus and hit "Download". The progress bar shown may not accurately represent the state of the download, since we won't know how many comments there are until we've finished searching. Downloading comments from many subreddits or over a large time range may take a long time. After the download finishes, you'll be redirected to a list of all downloaded corpora.

4. Create a lexicon to analyze the corpus with. A lexicon is a set of words paired with their ground-truth sentiment values. For more information about lexica and methodologies for creating good ones, refer to the [VADER Readme](https://github.com/cjhutto/vaderSentiment). Click the "Lexica" tab in the sidebar and click "New lexicon". Enter a name for the lexicon and enter a list of word/sentiment score pairs separated by a semicolon, one per line. Click "Confirm Selections".

5. Create a "report" by clicking the "reports" tab in the sidebar and clicking "New Report". On the left side, select a corpus, and on the right side, select one or more lexica to use to analyze that corpus. Enter a name for your report and click "Confirm Selections".

6. Finally, click "Run Report" to start the analysis. Especially with large corpora, the analysis may take a while. Check "Include body of comments in report" if you'd like the full text of the Reddit comments to be included in the TSV export, but keep in mind you'll have to re-run the report after changing this setting. After the report finishes, you can click "Export TSV" to export the results to a file.

## Running PogNLP from source

Clone the repository and `cd` to it:

```
git clone 'https://github.com/Reddit-NLP/reddit-nlp.git'
cd reddit-nlp
```

To run from source, first install [Poetry](https://python-poetry.org/):

```
pip install --user poetry
```

Then, install the dependencies:

```
poetry install
```

And run the application:

```
poetry run pognlp
```

### Windows users: Read this before running from source or attempting to package for distribution!

For reasons unknown to us, the Windows distribution of Python omits some important files that are required to run or package PogNLP. This GitHub issue has some discussion of the problem: https://github.com/serwy/tkthread/issues/2. The quick fix is as follows:

1. Download this zip file containing the missing files: [thread2.8.4.zip](https://github.com/serwy/tkthread/files/4258625/thread2.8.4.zip).
2. Determine the path to your Tcl installation. This can be done by running the included script `get-tcl-path.py`:

```
python get-tcl-path.py
```

The script will print a path such as `C:\Users\user\AppData\Local\Programs\Python\Python39\tcl\tcl8.6`.

3. Extract `thread2.8.4.zip` to a directory within this path.

If these steps are followed correctly, the program should start without errors when you run `poetry run pognlp`. If the files aren't installed, it will crash with the error: `_tkinter.TclError: can't find package Thread`.

## Packaging

PogNLP can be packaged into a distributable executable using [PyInstaller](https://www.pyinstaller.org/). To build for your system, run:

```
poetry run pyinstaller --noconfirm pognlp.spec
```

If GNU Make is available, you can instead simply run `make`.

The above command will create a self-contained, portable executable in `dist/` (`pognlp`, `pognlp.exe`, or `pognlp.app` depending on your platform). Despite our best efforts, a macOS .app built on one system is unlikely to run on other systems.
