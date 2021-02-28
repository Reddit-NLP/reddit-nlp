from tkthread import tk
import tkinter.font as f

import pognlp.util as util
import pognlp.view.common as common
from pognlp.model.report import Report
import pognlp.view.theme as theme


class ReportListView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=theme.background_color)

        self.selected_report = util.Observable(None)
        self.report_names = frozenset()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.listbox = tk.Listbox(
            self,
            relief="flat",
            height=5,
            borderwidth=0,
            fg="#000000",
            bg=theme.background_color_accent,
            bd=0,
            width=100,
            exportselection=0,
            font=f.Font(family=theme.font_family, size=15),
        )
        self.listbox.bind("<<ListboxSelect>>", self.on_select)  # select report

        self.listbox.grid(column=0, row=1, sticky="nesw")

        top_frame = tk.Frame(self)
        top_frame.configure(bg=theme.background_color_accent)
        top_frame.grid(column=0, row=0, sticky="ew")
        top_frame.grid_columnconfigure(0, minsize=100, weight=1)
        top_frame.grid_columnconfigure(1, minsize=100, weight=1)
        top_frame.grid_columnconfigure(2, minsize=100, weight=1)
        top_frame.grid_rowconfigure(0, minsize=100, weight=1)

        self.open_button = common.Button(
            top_frame,
            self.open_report,
            "Open Selected",
        )
        self.open_button.grid(column=0, row=0)

        create_report_button = common.Button(
            top_frame, self.create_report, "New Report"
        )
        create_report_button.grid(column=1, row=0)

        self.delete_button = common.Button(
            master=top_frame,
            command=lambda: self.controller.delete_report(self.selected_report.get()),
            text="Delete Selected",
        )
        self.delete_button.grid(column=2, row=0)

        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(column=1, row=1, sticky="ns")

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.controller.reports.subscribe(self.update_listbox)
        self.selected_report.subscribe(self.update_common)

    def open_report(self):
        self.controller.set_current_report(self.selected_report.get())
        self.controller.set_current_frame("ReportView")

    def create_report(self):
        self.controller.set_current_frame("CreateReportView")

    def update_listbox(self, reports):
        new_report_names = frozenset(reports.keys())
        if frozenset(self.report_names) == new_report_names:
            return

        if self.selected_report.get() not in new_report_names:
            self.selected_report.set(None)

        self.report_names = list(reports.keys())

        self.listbox.delete(0, tk.END)
        for report_name in self.report_names:
            self.listbox.insert(tk.END, report_name)

    def update_common(self, selected_report):
        state = tk.DISABLED if selected_report is None else tk.NORMAL
        self.open_button["state"] = state
        self.delete_button["state"] = state

    def on_select(self, event):
        selection = event.widget.curselection()
        if selection:
            [report_index] = selection
            self.selected_report.set(self.report_names[report_index])
