from tkthread import tk

import pognlp.util as util
import pognlp.view.buttons as buttons
from pognlp.model.report import Report
import pognlp.view.theme as theme


class ReportListView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=theme.background_color)

        self.report_names = frozenset()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(self)
        self.listbox.grid(column=0, row=0, sticky="nesw")

        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(column=1, row=0, sticky="ns")

        # for values in range(100):
        #     self.listbox.insert(tk.END, values)

        self.listbox.config(yscrollcommand=scrollbar.set)

        scrollbar.config(command=self.listbox.yview)

        self.controller.reports.subscribe(self.update_listbox)

    def update_listbox(self, reports):
        new_report_names = frozenset(report.name for report in reports)
        if self.report_names == new_report_names:
            return

        self.report_names = new_report_names

        self.listbox.delete(0, tk.END)
        for report_name in self.report_names:
            self.listbox.insert(tk.END, report_name)

        # top_frame.configure(bg=theme.background_color_accent)
        # top_frame.grid(sticky="ew")
        # top_frame.grid_columnconfigure(0, weight=1)
        # top_frame.grid_columnconfigure(1, weight=1)
        # top_frame.grid_columnconfigure(2, weight=1)
        # top_frame.grid_rowconfigure(0, minsize=100, weight=1)
        # # top_frame.pack_propagate(False)

        # run_report_button = buttons.Buttons(
        #     top_frame,
        #     self.run_report,
        #     "Run Report",
        # )
        # run_report_button.grid(row=0, column=0)

        # report_results = tk.Label(self)
        # report_results.grid(row=1, column=0, sticky="nsew")


class ReportView(tk.Frame):
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
        run_report_button.grid(row=0, column=0)

        report_results = tk.Label(self)
        report_results.grid(row=1, column=0, sticky="nsew")

    def run_report(self):
        util.run_thread()
