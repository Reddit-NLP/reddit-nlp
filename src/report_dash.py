import tkinter as tk
import buttons
import sidebar as listbox

from report import Report
import util
import theme


class ReportDashboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=theme.background_color)

        # top_navbar
        top_frame = tk.Frame(self)
        top_frame.configure(bg=theme.background_color_accent)
        top_frame.pack_propagate(False)

        run_report_button = buttons.Buttons(
            top_frame,
            self.run_report,
            "Run Report",
        )

        top_frame.grid(row=0, column=1, columnspan=4)

    def run_report(self):
        print("run report!")

    def update(self):
        pass
