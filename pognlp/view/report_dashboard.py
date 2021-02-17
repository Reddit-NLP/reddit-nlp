from tkthread import tk

import pognlp.util as util
import pognlp.view.buttons as buttons
from pognlp.model.report import Report
import pognlp.view.theme as theme


class ReportDashboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=theme.background_color)

        self.grid_columnconfigure(0, weight=1)

        # top_navbar
        top_frame = tk.Frame(self)
        top_frame.configure(bg=theme.background_color_accent)
        top_frame.grid(sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=1)
        top_frame.grid_rowconfigure(0, minsize=100, weight=1)
        # top_frame.pack_propagate(False)

        run_report_button = buttons.Buttons(
            top_frame,
            self.run_report,
            "Run Report",
        )
        run_report_button.grid(row=0, column=1)

    def run_report(self):
        print("run report!")

    def update(self):
        pass
