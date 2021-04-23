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

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        top_frame = tk.Frame(self)
        top_frame.configure(bg=theme.background_color)
        top_frame.grid(column=0, row=0, sticky="ns")
        top_frame.grid_columnconfigure(0, weight=1, minsize=400)
        top_frame.grid_columnconfigure(1, weight=1)

        # labels
        self.reddit_label = common.Label(top_frame, text="Download from Reddit")
        self.reddit_label.grid(columnspan=2, sticky="new")

        self.start_label = common.Label(
            top_frame, text="Start Date and (optional) Time"
        )
        self.start_label.grid(column=0, row=1, sticky="new")
        self.end_label = common.Label(top_frame, text="End Date and (optional) Time")
        self.end_label.grid(column=0, row=2, sticky="new")
        self.subs_label = common.Label(top_frame, text="Subreddit(s), one per line")
        self.subs_label.grid(column=0, row=3, sticky="new")

        self.client_id_label = common.Label(top_frame, text="Reddit Client ID")
        self.client_id_label.grid(column=0, row=4, sticky="new")
        self.client_secret_label = common.Label(top_frame, text="Reddit Client Secret")
        self.client_secret_label.grid(column=0, row=5, sticky="new")

        self.name_label = common.Label(top_frame, text="Corpus Name")
        self.name_label.grid(column=0, row=6, sticky="new")

        # entries
        self.start_entry = common.Entry(top_frame)
        self.start_entry.grid(column=1, row=1, sticky="new")
        self.end_entry = common.Entry(top_frame)
        self.end_entry.grid(column=1, row=2, sticky="new")
        self.subs_entry = common.Text(top_frame)
        self.subs_entry.grid(column=1, row=3, sticky="new")

        self.client_id_entry = common.Entry(top_frame)
        self.client_id_entry.grid(column=1, row=4, sticky="new")

        self.client_secret_entry = common.Entry(top_frame)
        self.client_secret_entry.grid(column=1, row=5, sticky="new")

        self.name_entry = common.Entry(top_frame)
        self.name_entry.grid(column=1, row=6, sticky="new")

        # download button and progress bar
        bottom_frame = tk.Frame(self)
        bottom_frame.configure(bg=theme.background_color_accent)
        bottom_frame.grid(column=0, row=1, sticky="nesw")
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(2, weight=1)

        self.download_button = common.Button(
            bottom_frame,
            command=self.download,
            text="Download",
        )
        self.download_button.configure(padx=10, pady=5)

        self.progress_bar = ttk.Progressbar(
            bottom_frame, orient=tk.HORIZONTAL, length=100, mode="indeterminate"
        )

        self.download_in_progress = util.Observable[bool](False)
        self.download_in_progress.subscribe(self.update_progress_bar, call=True)

        self.reset()

    def reset(self) -> None:
        """Reset the form to initial values"""
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.subs_entry.delete("1.0", tk.END)
        self.name_entry.delete(0, tk.END)

        # load last-used credentials from settings
        initial_client_id = self.controller.settings.get().get("REDDIT_CLIENT_ID") or ""
        initial_client_secret = (
            self.controller.settings.get().get("REDDIT_CLIENT_SECRET") or ""
        )

        self.client_id_entry.insert(tk.END, initial_client_id)
        self.client_secret_entry.insert(tk.END, initial_client_secret)

    def update_progress_bar(self, download_in_progress: bool) -> None:
        """Update download button and progress bar when download starts or stops"""
        if download_in_progress:
            self.download_button.grid_forget()
            if self.progress_bar["mode"] == "indeterminate":
                self.progress_bar.start()
            self.progress_bar.grid(column=1, row=4)
        else:
            self.progress_bar.grid_forget()
            self.progress_bar["mode"] = "indeterminate"
            self.progress_bar["value"] = 0
            self.progress_bar.stop()
            self.download_button.grid(column=1, row=4, sticky="sew")

    def progress_bar_cb(self, progress: int) -> None:
        """Called when progress is made on the download"""
        self.progress_bar["mode"] = "determinate"
        self.progress_bar["value"] = progress

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
        subs = [sub.split("/")[-1] for sub in text.split("\n") if sub]
        if not subs:
            tk.messagebox.showerror(
                "Error",
                "Please enter at least one subreddit to search.",
            )
            return
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

        self.download_in_progress.set(True)

        def download_and_update() -> None:
            assert start is not None
            assert end is not None
            corpus = RedditCorpus(
                name,
                subreddits=subs,
                start_time=start,
                end_time=end,
            )

            try:
                corpus.compile(
                    {
                        "client_id": client_id,
                        "client_secret": client_secret,
                    },
                    progress_cb=self.progress_bar_cb,
                )
                add_corpus = lambda: self.controller.add_corpus(corpus)
                self.controller.tkt(add_corpus)
                self.controller.tkt(self.controller.on_corpus_complete)
                self.controller.tkt(self.reset)
            except Exception as error:
                tk.messagebox.showerror("Error downloading!", str(error))
                corpus.delete()

            finally:
                self.download_in_progress.set(False)

        util.run_thread(download_and_update)
