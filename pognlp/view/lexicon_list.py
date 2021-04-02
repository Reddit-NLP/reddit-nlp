from tkthread import tk
import tkinter.font as f

import pognlp.util as util
import pognlp.view.common as common
import pognlp.view.theme as theme


class LexiconListView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=theme.background_color)

        self.selected_lexicon = util.Observable(None)
        self.lexicon_names = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.listbox = common.Listbox(
            self,
            exportselection=0,
        )
        self.listbox.bind("<<ListboxSelect>>", self.on_select)  # select lexicon

        self.listbox.grid(column=0, row=1, sticky="nesw")

        top_frame = tk.Frame(self)
        top_frame.configure(bg=theme.background_color_accent)
        top_frame.grid(column=0, row=0, sticky="ew")
        top_frame.grid_columnconfigure(0, minsize=100, weight=1)
        top_frame.grid_columnconfigure(1, minsize=100, weight=1)
        top_frame.grid_columnconfigure(2, minsize=100, weight=1)
        top_frame.grid_rowconfigure(0, minsize=100, weight=1)

        self.open_button = common.Button(
            top_frame,
            self.open_lexicon,
            "Edit Selected",
        )
        self.open_button.grid(column=0, row=0)

        create_lexicon_button = common.Button(
            top_frame, self.create_lexicon, "New lexicon"
        )
        create_lexicon_button.grid(column=1, row=0)

        self.delete_button = common.Button(
            master=top_frame,
            command=lambda: self.controller.delete_lexicon(self.selected_lexicon.get()),
            text="Delete Selected",
        )
        self.delete_button.grid(column=2, row=0)

        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(column=1, row=1, sticky="ns")

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.controller.lexica.subscribe(self.update_listbox)
        self.selected_lexicon.subscribe(self.update_common)

    def open_lexicon(self):
        self.controller.set_current_lexicon(self.selected_lexicon.get())
        self.controller.set_current_frame("CreateLexiconView")

    def create_lexicon(self):
        self.controller.set_current_lexicon(None)
        self.controller.set_current_frame("CreateLexiconView")

    def update_listbox(self, lexica):
        new_lexicon_names = frozenset(lexica.keys())
        if frozenset(self.lexicon_names) == new_lexicon_names:
            return

        if self.selected_lexicon.get() not in new_lexicon_names:
            self.selected_lexicon.set(None)

        self.lexicon_names = list(lexica.keys())

        self.listbox.delete(0, tk.END)
        for lexicon_name in self.lexicon_names:
            self.listbox.insert(tk.END, lexicon_name)

    def update_common(self, selected_lexicon):
        state = tk.DISABLED if selected_lexicon is None else tk.NORMAL
        self.open_button["state"] = state
        self.delete_button["state"] = state

    def on_select(self, event):
        selection = event.widget.curselection()
        if selection:
            [lexicon_index] = selection
            self.selected_lexicon.set(self.lexicon_names[lexicon_index])
