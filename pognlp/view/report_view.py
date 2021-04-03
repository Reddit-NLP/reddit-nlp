from tkthread import tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pognlp.view.theme as theme
import pognlp.view.common as common
import pognlp.util as util


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

    def make_figure(self):
        df = self.report.get_results()
        df.sort_values("timestamp", ascending=False)

        if df is None:
            return

        fig = plt.figure()
        axes = fig.add_subplot(111)

        # Not sure why, but we need to invert the x axis so left -> right is past -> present.
        axes.invert_xaxis()

        axes.set_title("Compound Sentiment Scores over Time")
        axes.set_xlabel("Datetime")
        axes.set_ylabel("Sentiment Score")

        compound_keys = [
            key for key in list(df.columns.values) if key.endswith("compound")
        ]

        df.plot(ax=axes, x="timestamp", y=compound_keys)

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
        else:
            run_report_button.grid(column=0, row=3)

        if self.report.complete:
            # report_results = common.Label(
            #     frame, text=self.report.get_results(), justify=tk.LEFT
            # )
            # report_results.grid(column=0, row=4)
            figure = self.make_figure()
            self.canvas = FigureCanvasTkAgg(figure, master=frame)
            self.canvas.draw()

            canvas_widget = self.canvas.get_tk_widget()
            canvas_widget.grid(column=0, row=4, sticky="nesw")

    def run_progress_cb(self, progress):
        self.run_progress["value"] = progress

    def run_report(self):
        self.run_in_progress = True
        self.update_dashboard(None)

        def run_and_update():
            self.report.run(
                progress_cb=lambda progress: self.controller.tkt(
                    self.run_progress_cb, progress
                )
            )
            self.run_in_progress = False
            self.controller.tkt(self.controller.reports.update)

        util.run_thread(run_and_update)
