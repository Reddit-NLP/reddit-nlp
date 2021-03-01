import os
from tkthread import tk, TkThread
import tkinter.font as font
import sys

import pognlp.util as util

from pognlp.model.corpus import Corpus, RedditCorpus
from pognlp.model.report import Report
from pognlp.model.lexicon import Lexicon

from pognlp.view.sidebar import Sidebar
from pognlp.view.home import HomeView
from pognlp.view.lexica import LexicaView
from pognlp.view.create_report import CreateReportView
from pognlp.view.report_list import ReportListView
from pognlp.view.report_view import ReportView


class AppView(tk.Frame):
    def __init__(self, parent, controller, current_frame, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        sidebar = Sidebar(parent=self, controller=controller)
        sidebar.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="ns")

        content = tk.Frame(self)
        content.grid(column=1, row=0, columnspan=3, rowspan=3, sticky="nesw")
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # this will contain all frames so they will be available
        # to raise
        for F in (HomeView, LexicaView, CreateReportView, ReportListView, ReportView):
            page_name = F.__name__
            frame = F(parent=content, controller=controller)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        current_frame.subscribe(self.update_current_frame)

    def update_current_frame(self, current_frame: str) -> None:
        self.frames[current_frame].tkraise()


class App(tk.Tk):
    """ Root level controller"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.tkt = TkThread(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_frame = util.Observable("HomeView")

        self.reports = util.Observable(
            {report_name: Report.load(report_name) for report_name in Report.ls()}
        )
        self.corpora = util.Observable(
            {corpus_name: Corpus.load(corpus_name) for corpus_name in Corpus.ls()}
        )
        self.lexica = util.Observable(
            {lexicon_name: Lexicon.load(lexicon_name) for lexicon_name in Lexicon.ls()}
        )
        self.current_report = util.Observable(None)

        print("reports", self.reports.get())
        print("lexica", self.lexica.get())

        view = AppView(self, self, current_frame=self.current_frame)
        view.grid(row=0, column=0, sticky="nesw")

    def set_current_frame(self, frame_name):
        self.current_frame.set(frame_name)

    def set_current_report(self, current_report):
        self.current_report.set(current_report)

    def create_report(self, report_name, corpus_name, lexicon_names):
        if report_name in self.reports.get():
            raise ValueError("A report already exists with that name.")
        report = Report(
            name=report_name, corpus_name=corpus_name, lexicon_names=lexicon_names
        )
        reports = {
            **self.reports.get(),
            report_name: report,
        }
        self.reports.set(reports)

    def delete_report(self, report_to_delete):
        reports = self.reports.get()
        self.reports.set(
            {
                name: report
                for name, report in reports.items()
                if name != report_to_delete
            }
        )
        reports[report_to_delete].delete()


def main():
    app = App()
    app.mainloop()


# starts the mainloop
if __name__ == "__main__":
    main()
