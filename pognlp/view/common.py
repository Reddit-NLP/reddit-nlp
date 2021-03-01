import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as f

import pognlp.view.theme as theme


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
    """Adapted from https://blog.tecladocode.com/tkinter-scrollable-frames/"""

    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        canvas = tk.Canvas(self, bg=theme.background_color)
        canvas.grid(column=0, row=0, sticky="nesw")
        canvas.grid_columnconfigure(0, weight=1)
        canvas.grid_rowconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar.grid(column=1, row=0, sticky="ns")

        self.scrollable_frame = tk.Frame(canvas, bg=theme.background_color)
        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        self.scrollable_frame.grid(column=0, row=0, sticky="nesw")

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
