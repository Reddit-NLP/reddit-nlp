from tkthread import tk
import tkinter.font as f

import pognlp.util as util
import pognlp.view.common as common
import pognlp.view.theme as theme


class CorpusListView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=theme.background_color)

        self.selected_corpus = util.Observable(None)
        self.corpus_names = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.listbox = common.Listbox(
            self,
            exportselection=0,
        )
        self.listbox.bind("<<ListboxSelect>>", self.on_select)  # select corpus

        self.listbox.grid(column=0, row=1, sticky="nesw")

        top_frame = tk.Frame(self)
        top_frame.configure(bg=theme.background_color_accent)
        top_frame.grid(column=0, row=0, sticky="ew")
        top_frame.grid_columnconfigure(0, minsize=100, weight=1)
        top_frame.grid_columnconfigure(1, minsize=100, weight=1)
        top_frame.grid_columnconfigure(2, minsize=100, weight=1)
        top_frame.grid_rowconfigure(0, minsize=100, weight=1)

        create_corpus_button = common.Button(
            top_frame, self.create_corpus, "New Reddit Corpus"
        )
        create_corpus_button.grid(column=0, row=0)

        self.delete_button = common.Button(
            master=top_frame,
            command=lambda: self.controller.delete_corpus(self.selected_corpus.get()),
            text="Delete Selected",
        )
        self.delete_button.grid(column=1, row=0)

        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(column=1, row=1, sticky="ns")

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.controller.corpora.subscribe(self.update_listbox)
        self.selected_corpus.subscribe(self.update_common)

    def create_corpus(self):
        self.controller.set_current_frame("CreateCorpusView")

    def update_listbox(self, corpora):
        new_corpus_names = frozenset(corpora.keys())
        if frozenset(self.corpus_names) == new_corpus_names:
            return

        if self.selected_corpus.get() not in new_corpus_names:
            self.selected_corpus.set(None)

        self.corpus_names = list(corpora.keys())

        self.listbox.delete(0, tk.END)
        for corpus_name in self.corpus_names:
            self.listbox.insert(tk.END, corpus_name)

    def update_common(self, selected_corpus):
        state = tk.DISABLED if selected_corpus is None else tk.NORMAL
        self.delete_button["state"] = state

    def on_select(self, event):
        selection = event.widget.curselection()
        if selection:
            [corpus_index] = selection
            self.selected_corpus.set(self.corpus_names[corpus_index])
