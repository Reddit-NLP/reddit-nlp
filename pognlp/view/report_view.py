from tkthread import tk
import tkinter.ttk as ttk
import numpy as np
from tkinter import filedialog as fd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import os
import shutil

import pognlp.view.theme as theme
import pognlp.view.common as common
import pognlp.util as util
from pognlp.model.lexicon import DefaultLexicon


class ReportView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=theme.background_color)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.content = common.ScrollableFrame(self)
        self.content.grid(sticky="nsew")

        self.report = None
        self.run_in_progress = False
        self.canvas = None

        self.controller.current_report.subscribe(self.update_dashboard)
        self.controller.reports.subscribe(self.update_dashboard)
        self.include_body = tk.BooleanVar()

    def make_timeseries_figure(self, df):
        df.sort_values("timestamp", ascending=False)

        fig = plt.figure()
        axes = fig.add_subplot(111)

        # Not sure why, but we need to invert the x axis so left -> right is past -> present.
        axes.invert_xaxis()

        axes.set_title("Compound Sentiment Scores over Time")

        compound_keys = [
            key for key in list(df.columns.values) if key.endswith("compound")
        ]

        df.plot(ax=axes, x="timestamp", y=compound_keys)
        axes.set_xlabel("Datetime")
        axes.set_ylabel("Sentiment Score")

        fig.autofmt_xdate()

        return fig

    def make_frequency_figure(self, df, lexicon_name):
        in_lexicon = df.loc[df["lexicon name"] == lexicon_name]

        if in_lexicon.empty:
            return None

        fig = plt.figure()
        axes = fig.add_subplot(111)

        y_pos = np.arange(len(in_lexicon))

        in_lexicon.plot(
            ax=axes,
            y="frequency per 10,000",
            x="lemmatized word",
            kind="barh",
            legend=None,
        )
        axes.set_title(f'Frequency per 10,000 of words in lexicon "{lexicon_name}"')
        axes.set_xlabel("Frequency per 10,000")
        axes.set_ylabel("Lemmatized Word")

        fig.autofmt_xdate()

        return fig

    def update_dashboard(self, _):
        current_report = self.controller.current_report.get()

        frame = self.content.interior
        frame.grid_columnconfigure(0, weight=1)

        for widget in frame.winfo_children():
            widget.destroy()

        if current_report is None:
            self.report = None
            return

        self.report = self.controller.reports.get()[current_report]

        common.Label(
            frame,
            text=self.report.name,
            justify=tk.LEFT,
            size=20,
        ).grid(column=0, row=0, sticky="w")

        common.Label(
            frame,
            text=f"Corpus: {self.report.corpus_name}",
            justify=tk.LEFT,
        ).grid(column=0, row=1, sticky="w")

        common.Label(
            frame,
            text=f"Lexica: {', '.join(self.report.lexicon_names)}",
            justify=tk.LEFT,
        ).grid(column=0, row=2, sticky="w")

        self.run_progress = ttk.Progressbar(
            frame, orient=tk.HORIZONTAL, length=100, mode="indeterminate"
        )
        run_report_button = common.Button(
            frame,
            self.run_report,
            "Run Report",
        )

        if self.run_in_progress:
            self.run_progress.grid(column=0, row=3)
            return

        run_report_button.grid(column=0, row=4)
        include_body_button = tk.Checkbutton(frame, text="Include body of comments in report", variable=self.include_body, onvalue=True, offvalue=False)
        include_body_button.grid(column=0, row=3)

        if self.report.complete:
            # report_results = common.Label(
            #     frame, text=self.report.get_results(), justify=tk.LEFT
            # )
            # report_results.grid(column=0, row=4)

            self.export_button = common.Button(
                frame,
                self.export,
                "Export",
            )
            self.export_button.grid(column=0, row=5)

            df = self.report.get_results()
            figure = self.make_timeseries_figure(df)
            self.canvas = FigureCanvasTkAgg(figure, master=frame)
            self.canvas.draw()

            canvas_widget = self.canvas.get_tk_widget()
            canvas_widget.grid(column=0, row=6, sticky="nesw")

            current_row = 7

            for lexicon_name in self.report.lexicon_names:
                if lexicon_name == DefaultLexicon.name:
                    continue

                df = self.report.get_frequencies()
                figure = self.make_frequency_figure(df, lexicon_name)

                if figure is None:
                    continue

                canvas = FigureCanvasTkAgg(figure, master=frame)
                self.canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.grid(column=0, row=current_row, sticky="nesw")
                current_row += 1

    def run_progress_cb(self, progress):
        self.run_progress["value"] = progress

    def run_report(self):
        self.run_in_progress = True
        self.update_dashboard(None)

        def run_and_update():
            self.report.run(
                progress_cb=lambda progress: self.controller.tkt(
                    self.run_progress_cb, progress
                ), include_body=self.include_body.get()
            )
            self.run_in_progress = False
            self.controller.tkt(self.controller.reports.update)

        util.run_thread(run_and_update)
    
    def export(self):
        dest = fd.asksaveasfilename()
        shutil.copyfile(self.report.output_path, dest)
        

