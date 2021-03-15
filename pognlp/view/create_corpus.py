import tkinter as tk
import tkinter.messagebox as messagebox
import dateparser
from tkinter import font
import pognlp.view.theme as theme
import pognlp.view.common as common
from pognlp.model.corpus import Corpus, RedditCorpus
from pognlp.model.lexicon import Lexicon


class CreateCorpusView(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller
        self.configure(bg=theme.background_color)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # labels
        self.reddit_label = common.Label(self, text="Download from Reddit")
        self.reddit_label.grid(columnspan=2, sticky="new")
        self.start_label = common.Label(self, text="Start Date and (optional) Time")
        self.start_label.grid(column=0, row=1, sticky="new")
        self.end_label = common.Label(self, text="End Date and (optional) Time")
        self.end_label.grid(column=0, row=2, sticky="new")
        self.subs_label = common.Label(self, text="Subreddit(s)")
        self.subs_label.grid(column=0, row=3, sticky="new")
        self.name_label = common.Label(self, text="Corpus Name")
        self.name_label.grid(column=0, row=4, sticky="new")

        self.start_entry = common.Entry(self)
        self.start_entry.grid(column=1, row=1, sticky="new")
        self.end_entry = common.Entry(self)
        self.end_entry.grid(column=1, row=2, sticky="new")
        self.subs_entry = tk.Text(self)
        self.subs_entry.grid(column=1, row=3, sticky="new")
        self.name_entry = common.Entry(self)
        self.name_entry.grid(column=1, row=4, sticky="new")

        # button
        bottom_frame = tk.Frame(self)
        bottom_frame.configure(bg=theme.background_color_accent)
        bottom_frame.grid(column=0, columnspan=2, sticky="nesw")
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(2, weight=1)

        download_button = common.Button(
             bottom_frame,
             command=self.download,
             text="Download",
        )
        download_button.grid(column=1, row=4, sticky="sew")

        download_button.configure(padx=10, pady=5)

    def download(self):
        start = dateparser.parse(self.start_entry.get())
        end = dateparser.parse(self.end_entry.get())
        name = self.name_entry.get()
        if not start or not end:
            tk.messagebox.showerror("Error","Please check that date/time format is recognizably valid.")
            return
        if not name:
            tk.messagebox.showerror("Error","Please enter a name.")
            return
        text = self.subs_entry.get('1.0','end')
        subs = text.split('\n')
        for subreddit in subs:
            if ',' in subreddit:
                tk.messagebox.showerror("Error","Please enter subreddits as a vertical list with no special characters.")
                return