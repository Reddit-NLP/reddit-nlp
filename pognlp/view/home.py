import tkinter as tk

import pognlp.view.common as common
import pognlp.view.theme as theme


class HomeView(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller
        self.configure(bg=theme.background_color)

        self.grid_columnconfigure(0, weight=1)

        # top_navbar
        top_frame = tk.Frame(self)
        top_frame.configure(bg=theme.background_color_accent)
        top_frame.grid(sticky="ew")
        # top_frame.pack_propagate(False)

        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=1)
        top_frame.grid_rowconfigure(0, minsize=100, weight=1)

        # top_navbar common
        download_button = common.Button(
            top_frame,
            command=lambda: printme(),
            text="Download New Data",
        )
        download_button.configure(padx=10, pady=10)

        create_report_button = common.Button(
            top_frame,
            command=lambda: controller.set_current_frame("CreateReportView"),
            text="Create New Report",
        )
        create_report_button.configure(padx=10, pady=10)

        lexicon_button = common.Button(
            top_frame,
            command=lambda: printme(),
            text="Create New Lexicon",
        )
        lexicon_button.configure(padx=10, pady=10)

        top_frame.grid(row=0, column=0, columnspan=1)
        download_button.grid(row=0, column=0)
        create_report_button.grid(row=0, column=1)
        lexicon_button.grid(row=0, column=2)

        welcome_header = common.Label(self, text="Welcome!", justify=tk.LEFT, size=20)
        welcome_header.grid(column=0, row=1)

        welcome_message = common.Label(
            self,
            text="To get started, select 'Download New Data' or 'Create New Lexicon'.",
            justify=tk.LEFT,
            size=12,
        )
        welcome_message.grid(column=0, row=2)


def printme():
    print(1)
