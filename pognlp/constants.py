"""Global constants"""

import os

from appdirs import user_data_dir

app_name = "PogNLP"
app_author = "PogNLP"

# TODO make user agent customizable in settings
reddit_user_agent = "linux:org.reddit-nlp.reddit-nlp:v0.1.0 (by /u/YeetoCalrissian)"

storage_path = os.path.join(user_data_dir(app_name, app_author))
os.makedirs(storage_path, exist_ok=True)

settings_path = os.path.join(storage_path, "settings.toml")

corpora_path = os.path.join(storage_path, "corpora")

lexica_path = os.path.join(storage_path, "lexica")

reports_path = os.path.join(storage_path, "reports")
