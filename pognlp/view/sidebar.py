"""Sidebar frame for navigating among pages"""

import tkinter as tk
import tkinter.font as f
from typing import Any, Callable, TYPE_CHECKING

import pognlp.view.theme as theme

if TYPE_CHECKING:
    from pognlp.app import App


class SideListbox(tk.Listbox):
    """Single entry in the sidebar"""

    def __init__(
        self,
        master: tk.Frame,
        text: str,
        on_select: Callable[[Any], None],
        **kw: Any,
    ):
        self.default_background = theme.accent_color
        tk.Listbox.__init__(
            self,
            master=master,
            relief="flat",
            height=0,  # height=0 sets it so the listboxes are wrapped around their items
            borderwidth=0,
            fg=theme.background_color_accent,
            bg=self.default_background,
            bd=0,
            width=13,
            exportselection=0,
            font=f.Font(family="Shree Devanagari 714", size=15),
            **kw,
        )

        self.insert(0, f"  {text}")

        self.bind("<<ListboxSelect>>", on_select)

        # binds these functions on mouse enter, motion, or leave
        self.bind("<Enter>", self.snap_highlight_to_mouse)
        self.bind("<Motion>", self.snap_highlight_to_mouse)
        self.bind("<Leave>", self.unhighlight)

    def snap_highlight_to_mouse(self, event: Any) -> None:
        """Called on mouse hover"""
        self.selection_clear(0, tk.END)
        self.itemconfig(
            self.nearest(event.y), bg=theme.highlight_color, fg=self.default_background
        )

    def unhighlight(self, event: Any) -> None:
        """Called on mouse leave"""
        self.selection_clear(0, tk.END)
        self.itemconfig(
            self.nearest(event.y),
            bg=self.default_background,
            fg=theme.background_color_accent,
        )


class Sidebar(tk.Frame):
    """Sidebar frame for navigating among pages"""

    def __init__(self, parent: tk.Frame, controller: "App", **kwargs: Any):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller

        self.configure(bg=theme.accent_color)

        self.grid_rowconfigure(0, minsize=100)
        self.grid_rowconfigure(1, minsize=20)
        self.grid_rowconfigure(2, minsize=20)
        self.grid_rowconfigure(3, minsize=20)

        # items for navbar
        home_item = SideListbox(
            master=self,
            text="Home",
            on_select=lambda _: controller.set_current_frame("HomeView"),
        )
        home_item.grid(column=0, row=1)

        corpora_item = SideListbox(
            master=self,
            text="Corpora",
            on_select=lambda _: controller.set_current_frame("CorpusListView"),
        )
        corpora_item.grid(column=0, row=2)

        lexica_item = SideListbox(
            master=self,
            text="Lexica",
            on_select=lambda _: controller.set_current_frame("LexiconListView"),
        )
        lexica_item.grid(column=0, row=3)

        reports_item = SideListbox(
            master=self,
            text="Reports",
            on_select=lambda _: controller.set_current_frame("ReportListView"),
        )
        reports_item.grid(column=0, row=4)
