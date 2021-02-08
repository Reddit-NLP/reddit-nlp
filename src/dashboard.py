import tkinter as tk
import buttons

import theme


class Dashboard(tk.Frame):
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

        # top_navbar buttons
        download_button = buttons.Buttons(
            top_frame,
            lambda: printme(),
            "Download New Data",
        )
        download_button.configure(padx=10, pady=10)

        create_report_button = buttons.Buttons(
            top_frame,
            lambda: controller.show_frame("CreateReportForm"),
            "Create New Report",
        )
        create_report_button.configure(padx=10, pady=10)

        lexicon_button = buttons.Buttons(
            top_frame,
            lambda: printme(),
            "Create New Lexicon",
        )
        lexicon_button.configure(padx=10, pady=10)

        top_frame.grid(row=0, column=0, columnspan=1)
        download_button.grid(row=0, column=0)
        create_report_button.grid(row=0, column=1)
        lexicon_button.grid(row=0, column=2)


def printme():
    print(1)
