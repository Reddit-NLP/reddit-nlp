import tkinter as tk
import tkinter as tk
from tkinter import font
import pognlp.view.theme as theme
import pognlp.view.buttons as buttons
from pognlp.model.corpus import Corpus, RedditCorpus
from pognlp.model.lexicon import Lexicon


class CreateReportView(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller
        self.configure(bg=theme.background_color)

        # self.report_names = frozenset()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.corpora = tk.Label(self, text="Select a Corpus")
        self.corpora.grid(column=0, row=0, rowspan=1, sticky="sew")
        self.lexica = tk.Label(self, text="Select a Lexicon")
        self.lexica.grid(column=1, row=0, rowspan=1, sticky="sew")

        self.corpus_listbox = tk.Listbox(self)
        self.corpus_listbox.grid(column=0, row=1, sticky="nsew")
        # add corpora to "select a corpus" list
        self.corpus_listbox.insert(tk.END, self.controller.corpora.get())

        self.lexicon_listbox = tk.Listbox(self)
        self.lexicon_listbox.grid(column=1, row=1, sticky="nsew")
        # add lexica to "select a lexicon" list
        self.lexicon_listbox.insert(tk.END, self.controller.lexica.get())

        #TODO: create button to confirm selections (use selections to create report, nav to ReportListView)
        
        

        # scrollbar = tk.Scrollbar(self)
        # scrollbar.grid(column=2, row=0, sticky="ns")
