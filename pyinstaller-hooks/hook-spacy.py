# from https://stackoverflow.com/a/60360900
# HOOK FILE FOR SPACY
from PyInstaller.utils.hooks import collect_all

# ----------------------------- SPACY -----------------------------
data = collect_all("spacy")

datas = data[0]
binaries = data[1]
hiddenimports = data[2]

# ----------------------------- THINC -----------------------------
data = collect_all("thinc")

datas += data[0]
binaries += data[1]
hiddenimports += data[2]

# ----------------------------- CYMEM -----------------------------
data = collect_all("cymem")

datas += data[0]
binaries += data[1]
hiddenimports += data[2]

# ----------------------------- PRESHED -----------------------------
data = collect_all("preshed")

datas += data[0]
binaries += data[1]
hiddenimports += data[2]

# ----------------------------- BLIS -----------------------------

data = collect_all("blis")

datas += data[0]
binaries += data[1]
hiddenimports += data[2]

# ----------------------------- en_core_web_sm -------------------

data = collect_all("en_core_web_sm")

datas += data[0]
binaries += data[1]
hiddenimports += data[2]

# This hook file is a bit of a hack - really, all of the libraries should be in seperate hook files. (Eg hook-blis.py with the blis part of the hook)
