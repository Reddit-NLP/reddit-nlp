import os
from tkthread import tk, TkThread
import tkinter.font as font
import sys

import pognlp.util as util

from pognlp.model.corpus import Corpus, RedditCorpus
from pognlp.model.report import Report

from pognlp.view.sidebar import Sidebar
from pognlp.view.home import HomeView
from pognlp.view.lexica import LexicaView
from pognlp.view.create_report import CreateReportView
from pognlp.view.report_list import ReportListView


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
        for F in (HomeView, LexicaView, CreateReportView, ReportListView):
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
            [Report.load(report_name) for report_name in Report.ls()]
        )

        view = AppView(self, self, current_frame=self.current_frame)
        view.grid(row=0, column=0, sticky="nesw")

        # TODO: for now, create a default corpus

        # print("all corpora: ", Corpus.ls())
        # try:
        #     default_corpus = Corpus.load("default-corpus")
        #     print("loaded default corpus from file")
        # except FileNotFoundError:
        #     default_corpus = RedditCorpus("default-corpus", ["gaming"])
        #     print("default corpus didn't exist, made a new one")

        # if not default_corpus.compiled:
        #     print("Downloading corpus from Reddit...")
        #     default_corpus.compile(os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"])

        # default_report = Report(default_corpus.name, [])
        # default_report.run()

    def set_current_frame(self, frame_name):
        self.current_frame.set(frame_name)


def main():
    app = App()
    app.mainloop()


# starts the mainloop
if __name__ == "__main__":
    main()
