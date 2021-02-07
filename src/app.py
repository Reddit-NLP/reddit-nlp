import os
import tkinter as tk
import tkinter.font as font
import sys


from corpus import Corpus, RedditCorpus
from report import Report
import side_listbox
import dashboard as dash
import create_report_form as form1
import dictionary_dash as dash2
import report_dash as dash3

class App(tk.Tk):
    #initializes the App 
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.grid(row=0, column=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_configure(rowspan=10, columnspan=10)
        
        self.frames = {}
        #this will contain all frames so they will be available
        #to raise
        for F in (dash.Dashboard, form1.CreateReportForm, dash2.DictionaryDashboard,
        dash3.ReportDashboard):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Dashboard")
        
        # TODO: for now, create a default corpus

               print("all corpora: ", Corpus.list())
               try:
                   default_corpus = Corpus.load("default-corpus")
                   print("loaded default corpus from file")
               except FileNotFoundError:
                   default_corpus = RedditCorpus("default-corpus", ["gaming"])
                   print("default corpus didn't exist, made a new one")

               if not default_corpus.compiled:
                   default_corpus.compile(os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"])

               default_report = Report(default_corpus.name, [])
               default_report.run()

        # TODO: for now, create a default corpus

        print("all corpora: ", Corpus.list())
        try:
            default_corpus = Corpus.load("default-corpus")
            print("loaded default corpus from file")
        except FileNotFoundError:
            default_corpus = RedditCorpus("default-corpus", ["gaming"])
            print("default corpus didn't exist, made a new one")

        if not default_corpus.compiled:
            default_corpus.compile(os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"])

        default_report = Report(default_corpus.name, [])
        default_report.run()

    #function to raise a specific frame
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

  

#starts the mainloop
if __name__=="__main__":

    app = App() 
    app.mainloop()



