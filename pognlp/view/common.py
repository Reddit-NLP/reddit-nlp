from sys import platform
from functools import partial
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as f

import pognlp.view.theme as theme


class Text(tk.Text):
    def __init__(self, master, size=12, **kw):
        super().__init__(
            master,
            bg=theme.background_color,
            fg=theme.main_color,
            font=f.Font(family=theme.font_family, size=size),
            **kw,
        )


class Checkbutton(ttk.Checkbutton):
    def __init__(self, master, size=12, **kw):
        super().__init__(
            master,
            onvalue=True,
            offvalue=False,
            **kw,
        )


class Entry(tk.Entry):
    def __init__(self, master, size=12, **kw):
        super().__init__(
            master,
            bg=theme.background_color,
            fg=theme.main_color,
            font=f.Font(family=theme.font_family, size=size),
            **kw,
        )


class Label(tk.Label):
    def __init__(self, master, size=12, **kw):
        super().__init__(
            master,
            bg=theme.background_color,
            fg=theme.main_color,
            font=f.Font(family=theme.font_family, size=size),
            **kw,
        )


class Listbox(tk.Listbox):
    def __init__(self, master, size=15, **kw):
        super().__init__(
            master,
            relief="flat",
            borderwidth=0,
            fg="#000000",
            bg=theme.background_color_accent,
            bd=0,
            width=100,
            font=f.Font(family=theme.font_family, size=15),
            **kw,
        )


class Button(tk.Button):
    def __init__(
        self,
        master,
        command=None,
        text=None,
        font_family="PingFang TC",
        color=theme.main_color,
        background_color=theme.background_color_accent,
        active_color=theme.highlight_color,
        **kw
    ):
        tk.Button.__init__(self, master=master, command=command, **kw)

        self.color = color
        self.active_color = active_color

        self["text"] = text
        font = f.Font(family=font_family)
        self["font"] = font
        self["foreground"] = color
        self["background"] = background_color
        self["activeforeground"] = active_color

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["foreground"] = self.active_color

    def on_leave(self, e):
        self["foreground"] = self.color


class ScrollableFrame(ttk.Frame):
    """
    A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    * This comes from a different naming of the the scrollwheel 'button', on different systems.
    """

    def __init__(self, parent, *args, **kw):

        super().__init__(parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        self.canvas = tk.Canvas(
            self,
            bd=0,
            bg=theme.background_color,
            highlightthickness=0,
            yscrollcommand=self.vscrollbar.set,
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        self.vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = tk.Frame(self.canvas, bg=theme.background_color)
        self.interior_id = self.canvas.create_window(
            0, 0, window=self.interior, anchor=tk.NW
        )

        self.interior.bind("<Configure>", self._configure_interior)
        self.canvas.bind("<Configure>", self._configure_canvas)
        self.canvas.bind("<Enter>", self._bind_to_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_from_mousewheel)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar

    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)

        if self.interior.winfo_reqwidth() != self.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canvas.config(width=self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id, width=self.winfo_width())

    # This can now handle either windows or linux platforms
    def _on_mousewheel(self, event, scroll=None):

        if platform == "linux" or platform == "linux2":
            self.canvas.yview_scroll(int(scroll), "units")
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind_to_mousewheel(self, event):
        if platform == "linux" or platform == "linux2":
            self.canvas.bind_all("<Button-4>", partial(self._on_mousewheel, scroll=-1))
            self.canvas.bind_all("<Button-5>", partial(self._on_mousewheel, scroll=1))
        else:
            self.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event):

        if platform == "linux" or platform == "linux2":
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.unbind_all("<MouseWheel>")
