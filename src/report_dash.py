import tkinter as tk
import buttons
import sidebar as listbox


class ReportDashboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#ffffff")

        # top_navbar
        top_frame = tk.Frame(self)
        top_frame.configure(bg="#f2f3f4")
        top_frame.pack_propagate(False)

        top_frame.grid(row=0, column=1, columnspan=4)
