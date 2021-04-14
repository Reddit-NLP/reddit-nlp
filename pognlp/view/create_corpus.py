"""Create corpus form. Currently only supports Reddit corpora."""

import tkinter as tk
import tkinter.ttk as ttk
from typing import Any, TYPE_CHECKING

import dateparser

import pognlp.view.theme as theme
import pognlp.view.common as common
import pognlp.util as util
from pognlp.model.corpus import RedditCorpus

if TYPE_CHECKING:
    from pognlp.app import App


class CreateCorpusView(tk.Frame):
    """Form for creating a new Reddit corpus"""

    def __init__(self, parent: tk.Frame, controller: "App", **kwargs: Any):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller
        self.configure(bg=theme.background_color)
        # self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # labels
        self.reddit_label = common.Label(self, text="Download from Reddit")
        self.reddit_label.grid(columnspan=2, sticky="new")

        self.start_label = common.Label(self, text="Start Date and (optional) Time")
        self.start_label.grid(column=0, row=1, sticky="new")
        self.end_label = common.Label(self, text="End Date and (optional) Time")
        self.end_label.grid(column=0, row=2, sticky="new")
        self.subs_label = common.Label(self, text="Subreddit(s), one per line")
        self.subs_label.grid(column=0, row=3, sticky="new")

        self.client_id_label = common.Label(self, text="Reddit Client ID")
        self.client_id_label.grid(column=0, row=4, sticky="new")
        self.client_secret_label = common.Label(self, text="Reddit Client Secret")
        self.client_secret_label.grid(column=0, row=5, sticky="new")

        self.name_label = common.Label(self, text="Corpus Name")
        self.name_label.grid(column=0, row=6, sticky="new")

        # load last-used credentials from settings
        initial_client_id = self.controller.settings.get().get("REDDIT_CLIENT_ID") or ""
        initial_client_secret = (
            self.controller.settings.get().get("REDDIT_CLIENT_SECRET") or ""
        )

        # entries
        self.start_entry = common.Entry(self)
        self.start_entry.grid(column=1, row=1, sticky="new")
        self.end_entry = common.Entry(self)
        self.end_entry.grid(column=1, row=2, sticky="new")
        self.subs_entry = common.Text(self)
        self.subs_entry.grid(column=1, row=3, sticky="new")

        self.client_id_entry = common.Entry(self)
        self.client_id_entry.grid(column=1, row=4, sticky="new")
        self.client_id_entry.insert(tk.END, initial_client_id)

        self.client_secret_entry = common.Entry(self)
        self.client_secret_entry.grid(column=1, row=5, sticky="new")
        self.client_secret_entry.insert(tk.END, initial_client_secret)

        self.name_entry = common.Entry(self)
        self.name_entry.grid(column=1, row=6, sticky="new")

        # button
        bottom_frame = tk.Frame(self)
        bottom_frame.configure(bg=theme.background_color_accent)
        bottom_frame.grid(column=0, columnspan=2, sticky="nesw")
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(2, weight=1)

        self.download_button = common.Button(
            bottom_frame,
            command=self.download,
            text="Download",
        )
        self.download_button.configure(padx=10, pady=5)
        self.download_button.grid(column=1, row=4, sticky="sew")
        self.download_in_progress = False

        self.download_progress = ttk.Progressbar(
            bottom_frame, orient=tk.HORIZONTAL, length=100, mode="indeterminate"
        )

    def download_progress_cb(self, progress: int) -> None:
        """Called when progress is made on the download"""
        self.download_button.grid_forget()

        self.download_progress.grid(column=1, row=4)
        self.download_progress["value"] = progress

    def download(self) -> None:
        """Validate entered data and start the download"""
        start = dateparser.parse(self.start_entry.get())
        end = dateparser.parse(self.end_entry.get())
        name = self.name_entry.get()
        if None in (start, end):
            tk.messagebox.showerror(
                "Error", "Please check that date/time format is recognizably valid."
            )
            return
        if not name:
            tk.messagebox.showerror("Error", "Please enter a name.")
            return
        text = self.subs_entry.get("1.0", "end")
        subs = [sub for sub in text.split("\n") if sub]
        for subreddit in subs:
            if "," in subreddit:
                tk.messagebox.showerror(
                    "Error",
                    "Please enter one valid subreddit name per line, with no special characters.",
                )
                return

        client_id = self.client_id_entry.get().strip()
        client_secret = self.client_secret_entry.get().strip()
        if not client_id:
            tk.messagebox.showerror(
                "Error",
                "Please enter a Reddit Client ID.",
            )
            return
        if not client_secret:
            tk.messagebox.showerror(
                "Error",
                "Please enter a Reddit Client Secret.",
            )
            return

        self.controller.set_reddit_credentials(client_id, client_secret)

        self.download_in_progress = True

        def download_and_update() -> None:
            assert start is not None
            assert end is not None
            corpus = RedditCorpus(
                name,
                subreddits=subs,
                start_time=start,
                end_time=end,
            )
            corpus.compile(
                {
                    "client_id": client_id,
                    "client_secret": client_secret,
                },
                progress_cb=self.download_progress_cb,
            )

            add_corpus = lambda: self.controller.add_corpus(corpus)
            self.controller.tkt(add_corpus)

        util.run_thread(download_and_update)
