"""Create report form"""

import tkinter as tk
import tkinter.messagebox as messagebox
from typing import Any, Dict, List, TYPE_CHECKING, Union

import pognlp.view.theme as theme
import pognlp.view.common as common
from pognlp.model.corpus import Corpus
from pognlp.model.lexicon import DefaultLexicon, Lexicon

if TYPE_CHECKING:
    from pognlp.app import App


class CreateReportView(tk.Frame):
    """Page for creating a new report"""

    def __init__(self, parent: tk.Frame, controller: "App", **kwargs: Any):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller
        self.configure(bg=theme.background_color)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # labels
        self.corpus_label = common.Label(self, text="Select a Corpus")
        self.corpus_label.grid(column=0, row=0, rowspan=1, sticky="sew")
        self.lexicon_label = common.Label(
            self, text="Select Lexica (click to select multiple)"
        )
        self.lexicon_label.grid(column=1, row=0, rowspan=1, sticky="sew")

        self.corpus_listbox = common.Listbox(self, exportselection=0)
        self.corpus_listbox.grid(column=0, row=1, sticky="nsew")

        self.lexicon_listbox = common.Listbox(
            self, selectmode="multiple", exportselection=0
        )
        self.lexicon_listbox.grid(column=1, row=1, sticky="nsew")

        self.corpus_names: List[str] = []
        self.lexicon_names: List[str] = []

        self.controller.corpora.subscribe(self.update_corpora)
        self.controller.lexica.subscribe(self.update_lexica)

        # button
        bottom_frame = tk.Frame(self)
        bottom_frame.configure(bg=theme.background_color_accent)
        bottom_frame.grid(column=0, columnspan=2, sticky="nesw")
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(2, weight=1)

        report_name_label = common.Label(bottom_frame, text="Report Name:")
        report_name_label.grid(column=0, row=0)

        self.report_name_entry = common.Entry(bottom_frame)
        self.report_name_entry.grid(column=1, row=0, sticky="ns")

        report_params_button = common.Button(
            bottom_frame,
            command=self.create_report,
            text="Confirm Selections",
        )
        report_params_button.grid(column=2, row=0, sticky="ns")

        report_params_button.configure(padx=10, pady=5)

    def update_corpora(self, corpora: Dict[str, Corpus]) -> None:
        """Update the list of corpora when one is added or removed"""
        self.corpus_names = list(corpora.keys())
        self.corpus_listbox.delete(0, tk.END)

        # add corpora to "select a corpus" list
        for corpus_name in self.corpus_names:
            self.corpus_listbox.insert(tk.END, corpus_name)

    def update_lexica(self, lexica: Dict[str, Union[DefaultLexicon, Lexicon]]) -> None:
        """Update the list of lexica when one is added or removed"""
        self.lexicon_names = list(lexica.keys())

        self.lexicon_listbox.delete(0, tk.END)

        # add lexica to list
        for lexicon_name in self.lexicon_names:
            self.lexicon_listbox.insert(tk.END, lexicon_name)

    def create_report(self) -> None:
        """Validate entered data and create a new report"""
        report_name = self.report_name_entry.get()
        if not report_name:
            messagebox.showerror("Error", "Please enter a name.")
            return

        corpus_indices = self.corpus_listbox.curselection()
        if not corpus_indices:
            messagebox.showerror("Error", "Please select at a corpus.")
            return
        [corpus_index] = corpus_indices

        corpus_name = self.corpus_names[corpus_index]

        lexicon_indices = self.lexicon_listbox.curselection()
        if not lexicon_indices:
            tk.messagebox.showerror("Error", "Please select at least one lexicon.")
        lexicon_names = [self.lexicon_names[index] for index in lexicon_indices]

        try:
            self.controller.create_report(report_name, corpus_name, lexicon_names)
        except ValueError as error:
            tk.messagebox.showerror("Error", str(error))
            return

        self.report_name_entry.delete(0, tk.END)

        self.controller.set_current_report(report_name)
        self.controller.set_current_frame("ReportView")
