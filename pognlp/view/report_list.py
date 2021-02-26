from tkthread import tk
import tkinter.font as f

import pognlp.util as util
import pognlp.view.buttons as buttons
from pognlp.model.report import Report
import pognlp.view.theme as theme

class ReportListbox(tk.Listbox):
    def __init__(self, master, text, **kw):
        tk.Listbox.__init__(
            self,
            master=master,
            relief="flat",
            height=5,
            borderwidth=0,
            fg="#000000",
            bg=theme.background_color_accent,
            bd=0,
            width=100,
            exportselection=0,
            font=f.Font(family="Shree Devanagari 714", size=15),
            **kw,
        )
        report = Report.load(text)
        self.insert(0, f"  {report.name}")
        self.insert(1, f"  {report.corpus_name}")
        lexica_list = ""
        for lexica in report.lexicon_names:
            lexica_list = lexica_list + " " + lexica
        self.insert(2,f"  {lexica_list}")

        self.bind("<<ListboxSelect>>", lambda _: print(self.get(0)))#open report

class ReportListView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=theme.background_color)

        self.report_names = frozenset()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(self)
        #self.listbox.grid(column=0, row=0, sticky="nesw")

        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(column=2, row=0, sticky="ns")

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

        #self.listbox.delete(0, tk.END)
        x = 0
        for report_name in self.report_names:
            #self.listbox.insert(tk.END, report_name)
            list_item = ReportListbox(master = self, text = report_name)
            list_item.grid(column = 0, row = x, sticky = "nesw")
            delete_button = buttons.Buttons(master=self,command=delete_report(report_name),text="Delete")
            delete_button.grid(column = 1, row = x)
            x = x + 1

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
def delete_report(name):
    report_name = name
    return lambda: delete_report2(report_name)
def delete_report2(report_name):
    report = Report.load(report_name)
    print(report_name)
    #remove report from list
