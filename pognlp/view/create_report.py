import tkinter as tk
import tkinter as tk
from tkinter import font


class CreateReportView(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller
        self.configure(bg="red")
