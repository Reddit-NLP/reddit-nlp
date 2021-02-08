import os
import tkinter as tk
import tkinter.font as font
import sys


from corpus import Corpus, RedditCorpus
from report import Report
from sidebar import Sidebar
from dashboard import Dashboard
from dictionary_dash import DictionaryDashboard
from create_report_form import CreateReportForm
from report_dash import ReportDashboard


class App(tk.Tk):
    # initializes the App

    main_color = "#30009C"
    highlight_color = "#FB3552"

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nesw")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        # container.grid_configure(rowspan=10, columnspan=10)

        sidebar = Sidebar(parent=container, controller=self)
        sidebar.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="ns")

        content = tk.Frame(container)
        content.grid(column=1, row=0, columnspan=3, rowspan=3, sticky="nesw")
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)
        content.configure(bg="#ff00ff")

        self.frames = {}
        # this will contain all frames so they will be available
        # to raise
        for F in (Dashboard, DictionaryDashboard, CreateReportForm, ReportDashboard):
            # for F in (dash.Dashboard, form1.CreateReportForm, dash2.DictionaryDashboard, dash3.ReportDashboard):
            page_name = F.__name__
            frame = F(parent=content, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Dashboard")

        # TODO: for now, create a default corpus

    #         print("all corpora: ", Corpus.list())
    #         try:
    #             default_corpus = Corpus.load("default-corpus")
    #             print("loaded default corpus from file")
    #         except FileNotFoundError:
    #             default_corpus = RedditCorpus("default-corpus", ["gaming"])
    #             print("default corpus didn't exist, made a new one")

    #         if not default_corpus.compiled:
    #             default_corpus.compile(os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"])

    #         default_report = Report(default_corpus.name, [])
    #         default_report.run()

    # function to raise a specific frame
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()


# starts the mainloop
if __name__ == "__main__":

    app = App()
    app.mainloop()
