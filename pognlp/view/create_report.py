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
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # labels
        self.corpora = tk.Label(self, text="Select a Corpus")
        self.corpora.grid(column=0, row=0, rowspan=1, sticky="sew")
        self.lexica = tk.Label(self, text="Select a Lexicon")
        self.lexica.grid(column=1, row=0, rowspan=1, sticky="sew")

        self.corpus_listbox = tk.Listbox(self, exportselection=0)
        self.corpus_listbox.grid(column=0, row=1, sticky="nsew")
        # add corpora to "select a corpus" list
        self.corpus_listbox.insert(tk.END, self.controller.corpora.get())

        self.lexicon_listbox = tk.Listbox(self, exportselection=0)
        self.lexicon_listbox.grid(column=1, row=1, sticky="nsew")
        # add lexica to "select a lexicon" list
        self.lexicon_listbox.insert(tk.END, self.controller.lexica.get())

        sel_lex = self.lexicon_listbox.get(tk.ANCHOR)
        sel_cor = self.corpus_listbox.get(tk.ANCHOR)
        
        # button
        bottom_frame = tk.Frame(self)
        bottom_frame.configure(bg=theme.background_color_accent)
        bottom_frame.grid(column=1, sticky="ns")

        report_params_button = buttons.Buttons(
            bottom_frame,
            command=lambda: controller.set_current_frame("ReportListView"), #TODO: pass selections to analyzer
            text="Confirm Selections",
        )
        
        report_params_button.grid(sticky="ns")
        report_params_button.configure(padx=10, pady=5)
        

        # scrollbar = tk.Scrollbar(self)
        # scrollbar.grid(column=2, row=0, sticky="ns")
