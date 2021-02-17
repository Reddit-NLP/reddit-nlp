import tkinter as tk

import pognlp.view.theme as theme


class DictionaryDashboard(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller
        self.configure(bg=theme.background_color)

        # top_navbar
        # top_frame = tk.Frame(self)
        # top_frame.configure(bg="#f2f3f4")
        # top_frame.grid(column=0, row=0)
