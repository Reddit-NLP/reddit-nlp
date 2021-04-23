# PogNLP

## Release Notes

### PogNLP v1.0
New Features
- Allows data to be downloaded from Reddit
- Allows creation of custom dictionaries (lexica) to be created for the nlp algorithm
- Can run the nlp algorithm on downloaded data using created lexica

Bug Fixes
- Added error messages when the download is unsuccessful
- Added message to display when download is complete
- Fixed issues where you could not create multiple corpora without restarting the app

Known Bugs

## Install Information

### Running PogNLP

Portable executables for GNU/Linux, macOS, and Windows are available for download in the [Releases section](https://github.com/Reddit-NLP/reddit-nlp/releases).

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

The above command will create a self-contained, portable executable in `dist/` (`pognlp`, `pognlp.exe`, or `pognlp.app` depending on your platform).
