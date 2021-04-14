"""View for a single report"""

import shutil
import tkinter.ttk as ttk
from tkinter import filedialog as fd
from collections import defaultdict
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from tkthread import tk
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pognlp.view.theme as theme
import pognlp.view.common as common
import pognlp.util as util
from pognlp.model.lexicon import DefaultLexicon
from pognlp.model.report import Report

if TYPE_CHECKING:
    from pognlp.app import App


class ReportView(tk.Frame):
    """Run a single report, generate charts, export data"""

    def __init__(self, parent: tk.Frame, controller: "App"):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=theme.background_color)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.content = common.ScrollableFrame(self)
        self.content.grid(sticky="nsew")

        self.report: Optional[Report] = None
        self.run_progress: Optional[ttk.Progressbar] = None
        self.run_in_progress = False

        self.controller.current_report.subscribe(self.update_dashboard)
        self.controller.reports.subscribe(self.update_dashboard)
        self.include_body = tk.BooleanVar()

    @staticmethod
    def make_timeseries_figure(df: pd.DataFrame) -> matplotlib.figure.Figure:
        """Create a figure showing the compound sentiment scores as they change over time"""
        if df.empty:
            return None

        df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Resample the timeseries to smooth it out and interpolate missing data
        if len(df) > 20:
            df = (
                df.set_index("timestamp")
                .resample("6H")
                .mean()
                .interpolate("linear")
                .reset_index()
            )

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

        legend = axes.get_legend()

        # Create mappings between lines on the chart and the corresponding legend elements
        lines_by_legend_element: Dict[
            matplotlib.artist.Artist, matplotlib.lines.Line2D
        ] = {}
        legend_elements_by_line = defaultdict[
            matplotlib.lines.Line2D, List[matplotlib.artist.Artist]
        ](lambda: [])
        for legend_text, legend_line, line in zip(
            legend.get_texts(), legend.get_lines(), axes.get_lines()
        ):
            legend_text.set_picker(True)
            legend_line.set_picker(True)
            lines_by_legend_element[legend_line] = line
            lines_by_legend_element[legend_text] = line
            legend_elements_by_line[line].extend((legend_line, legend_text))

        # Hide/show series by clicking them in the legend
        # see https://matplotlib.org/stable/gallery/event_handling/legend_picking.html
        def on_pick(event: Any) -> None:
            legend_element = event.artist
            line = lines_by_legend_element[legend_element]
            visible = not line.get_visible()
            line.set_visible(visible)
            for element in legend_elements_by_line[line]:
                element.set_alpha(1.0 if visible else 0.2)
            fig.canvas.draw()

        fig.canvas.mpl_connect("pick_event", on_pick)

        fig.autofmt_xdate()

        return fig

    @staticmethod
    def make_frequency_figure(
        df: pd.DataFrame, lexicon_name: str
    ) -> matplotlib.figure.Figure:
        """Return a figure showing relative frequencies of the most frequent
        words in the corpus"""
        in_lexicon = df.loc[df["lexicon name"] == lexicon_name]

        if in_lexicon.empty:
            return None

        max_words_to_display = 20
        if len(in_lexicon) > max_words_to_display:
            in_lexicon = in_lexicon.nlargest(
                max_words_to_display, "frequency per 10,000"
            )

        fig = plt.figure()
        axes = fig.add_subplot(111)

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

    def update_dashboard(self, _: Any) -> None:
        """Reset the page when the current report changes"""
        frame = self.content.interior
        frame.grid_columnconfigure(0, weight=1)

        for widget in frame.winfo_children():
            widget.destroy()

        current_report = self.controller.current_report.get()

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
        include_body_button = common.Checkbutton(
            frame,
            text="Include body of comments in report",
            variable=self.include_body,
        )
        include_body_button.grid(column=0, row=3)

        if self.report.complete:
            export_button = common.Button(
                frame,
                self.export,
                "Export as TSV",
            )
            export_button.grid(column=0, row=5)

            current_row = 6

            df = self.report.get_results()
            figure = self.make_timeseries_figure(df)
            if figure is not None:
                canvas = FigureCanvasTkAgg(figure, master=frame)
                canvas.draw()

                canvas_widget = canvas.get_tk_widget()
                canvas_widget.grid(column=0, row=current_row, sticky="nesw")
                current_row += 1

            for lexicon_name in self.report.lexicon_names:
                if lexicon_name == DefaultLexicon.name:
                    continue

                df = self.report.get_frequencies()
                figure = self.make_frequency_figure(df, lexicon_name)

                if figure is None:
                    continue

                canvas = FigureCanvasTkAgg(figure, master=frame)
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.grid(column=0, row=current_row, sticky="nesw")
                current_row += 1

    def run_progress_cb(self, progress: int) -> None:
        """Update the progress bar as the report is run"""
        if self.run_progress is None:
            return
        self.run_progress["value"] = progress

    def run_report(self) -> None:
        """Start running the report in another thread"""

        if self.report is None:
            return

        report = self.report

        self.run_in_progress = True
        self.update_dashboard(None)

        def run_and_update() -> None:
            report.run(
                progress_cb=lambda progress: self.controller.tkt(
                    self.run_progress_cb, progress
                )
                and None,
                include_body=self.include_body.get(),
            )
            self.run_in_progress = False
            self.controller.tkt(self.controller.reports.update)

        util.run_thread(run_and_update)

    def export(self) -> None:
        """Export the report results to a user-specified location"""

        if self.report is None:
            return

        dest = fd.asksaveasfilename()
        if dest:
            shutil.copyfile(self.report.output_path, dest)
