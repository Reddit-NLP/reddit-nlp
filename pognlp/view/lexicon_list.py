"""View for the list of stored lexica"""

from typing import Dict, List, Optional, TYPE_CHECKING, Union

from tkthread import tk

import pognlp.util as util
import pognlp.view.common as common
import pognlp.view.theme as theme
from pognlp.model.lexicon import DefaultLexicon, Lexicon

if TYPE_CHECKING:
    from pognlp.app import App


class LexiconListView(tk.Frame):
    """View for the list of stored lexica"""

    def __init__(self, parent: tk.Frame, controller: "App"):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=theme.background_color)

        self.selected_lexicon = util.Observable[Optional[str]](None)
        self.lexicon_names: List[str] = []

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
            command=self.delete_lexicon,
            text="Delete Selected",
        )
        self.delete_button.grid(column=2, row=0)

        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(column=1, row=1, sticky="ns")

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.controller.lexica.subscribe(self.update_listbox)
        self.selected_lexicon.subscribe(self.update_common)

    def open_lexicon(self) -> None:
        """Open the selected lexicon in CreateLexiconView"""
        self.controller.set_current_lexicon(self.selected_lexicon.get())
        self.controller.set_current_frame("CreateLexiconView")

    def create_lexicon(self) -> None:
        """Go to blank CreateLexiconView"""
        self.controller.set_current_lexicon(None)
        self.controller.set_current_frame("CreateLexiconView")

    def update_listbox(self, lexica: Dict[str, Union[Lexicon, DefaultLexicon]]) -> None:
        """Update the lexicon list when one is added or removed"""

        # If the set of lexicon names hasn't changed, don't update
        new_lexicon_names = frozenset(lexica.keys())
        if frozenset(self.lexicon_names) == new_lexicon_names:
            return

        if self.selected_lexicon.get() not in new_lexicon_names:
            self.selected_lexicon.set(None)

        self.lexicon_names = list(lexica.keys())

        self.listbox.delete(0, tk.END)
        for lexicon_name in self.lexicon_names:
            self.listbox.insert(tk.END, lexicon_name)

    def update_common(self, selected_lexicon: Optional[str]) -> None:
        """Disable buttons if selected_corpus is None, else enable"""
        state = tk.DISABLED if selected_lexicon is None else tk.NORMAL
        self.open_button["state"] = state
        self.delete_button["state"] = state

    def on_select(self, event: tk.Event) -> None:
        """Set selected_lexicon when the listbox selection changes"""
        selection = event.widget.curselection()
        if selection:
            [lexicon_index] = selection
            self.selected_lexicon.set(self.lexicon_names[lexicon_index])

    def delete_lexicon(self) -> None:
        """Delete the selected lexicon"""
        lexicon = self.selected_lexicon.get()
        if lexicon is None:
            return
        self.controller.delete_lexicon(lexicon)
