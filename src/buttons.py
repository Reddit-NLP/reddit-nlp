import tkinter as tk
import tkinter.font as f


class Buttons(tk.Button):
    def __init__(self, master, command, text, font, color, active_color, **kw):
        tk.Button.__init__(self, master=master, command=command, **kw)

        self.color = color
        self.active_color = active_color

        self["text"] = text
        font = f.Font(family=font)
        self["font"] = font
        self["foreground"] = color
        self["background"] = "#dddddd"
        self["activeforeground"] = active_color

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["foreground"] = self.active_color

    def on_leave(self, e):
        self["foreground"] = self.color
