"""View for the list of stored reports"""

from typing import Dict, List, Optional, TYPE_CHECKING

from tkthread import tk

import pognlp.util as util
import pognlp.view.common as common
import pognlp.view.theme as theme
from pognlp.model.report import Report

if TYPE_CHECKING:
    from pognlp.app import App


class ReportListView(tk.Frame):
    """View for the list of stored reports"""

    def __init__(self, parent: tk.Frame, controller: "App"):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=theme.background_color)

        self.selected_report = util.Observable[Optional[str]](None)
        self.report_names: List[str] = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.listbox = common.Listbox(
            self,
            exportselection=0,
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
            command=self.delete_report,
            text="Delete Selected",
        )
        self.delete_button.grid(column=2, row=0)

        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(column=1, row=1, sticky="ns")

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.controller.reports.subscribe(self.update_listbox)
        self.selected_report.subscribe(self.update_common)

    def open_report(self) -> None:
        """View the selected report"""
        self.controller.set_current_report(self.selected_report.get())
        self.controller.set_current_frame("ReportView")

    def create_report(self) -> None:
        """Go to create report view"""
        self.controller.set_current_frame("CreateReportView")

    def update_listbox(self, reports: Dict[str, Report]) -> None:
        """Update the listbox when the reports change"""

        # Don't update if the set of names hasn't changed

        new_report_names = frozenset(reports.keys())
        if frozenset(self.report_names) == new_report_names:
            return

        if self.selected_report.get() not in new_report_names:
            self.selected_report.set(None)

        self.report_names = list(reports.keys())

        self.listbox.delete(0, tk.END)
        for report_name in self.report_names:
            self.listbox.insert(tk.END, report_name)

    def update_common(self, selected_report: Optional[str]) -> None:
        """Disable buttons if selected_report is None, else enable"""
        state = tk.DISABLED if selected_report is None else tk.NORMAL
        self.open_button["state"] = state
        self.delete_button["state"] = state

    def on_select(self, event: tk.Event) -> None:
        """Set selected_report when the listbox selection changes"""
        selection = event.widget.curselection()
        if selection:
            [report_index] = selection
            self.selected_report.set(self.report_names[report_index])

    def delete_report(self) -> None:
        """Delete the selected report"""
        report = self.selected_report.get()
        if report is None:
            return
        self.controller.delete_report(report)
