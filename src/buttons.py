import tkinter as tk


class Buttons(tk.Button):
    def __init__(self, master, text, font, color, active_color, function, **kw):
        tk.Button.__init__(self, master = master, **kw)
        self.color = color
        self.active_color = active_color
        self["text"] = text
        self["font"] = font
        self["foreground"] = color
        self["activeforeground"] = active_color
        self["command"] = function

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["foreground"] = self.active_color
        
    def on_leave(self, e):
        self["foreground"] = self.color

        
        

