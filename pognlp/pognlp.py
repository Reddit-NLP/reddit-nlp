"""Main entry point, GUI setup, and root-level controller"""

from typing import Any, Dict, List, Optional, Tuple, Union

import rtoml as toml
from tkthread import tk, TkThread

from pognlp.model.corpus import Corpus
from pognlp.model.lexicon import DefaultLexicon, Lexicon
from pognlp.model.report import Report
from pognlp.view.corpus_list import CorpusListView
from pognlp.view.create_corpus import CreateCorpusView
from pognlp.view.create_lexicon import CreateLexiconView
from pognlp.view.create_report import CreateReportView
from pognlp.view.home import HomeView
from pognlp.view.lexicon_list import LexiconListView
from pognlp.view.report_list import ReportListView
from pognlp.view.report_view import ReportView
from pognlp.view.sidebar import Sidebar
import pognlp.constants as constants
import pognlp.util as util


class AppView(tk.Frame):
    """Contains all other views, keeps the current view on top"""

    def __init__(
        self,
        parent: tk.Frame,
        controller: tk.Tk,
        current_frame: util.Observable[str],
        **kwargs: Any,
    ):
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
        for F in (
            HomeView,
            LexiconListView,
            CreateReportView,
            CreateLexiconView,
            ReportListView,
            ReportView,
            CorpusListView,
            CreateCorpusView,
        ):
            page_name = F.__name__
            frame = F(parent=content, controller=controller)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        current_frame.subscribe(self.update_current_frame)

    def update_current_frame(self, current_frame: str) -> None:
        """"Raise the current frame when current_frame updates"""
        self.frames[current_frame].tkraise()


class App(tk.Tk):
    """ Root-level controller"""

    def __init__(self, *args: Any, **kwargs: Any):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("PogNLP")

        self.tkt = TkThread(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_frame = util.Observable[str]("HomeView")

        self.reports = util.Observable[Dict[str, Report]](
            {report_name: Report.load(report_name) for report_name in Report.ls()}
        )
        self.corpora = util.Observable[Dict[str, Corpus]](
            {corpus_name: Corpus.load(corpus_name) for corpus_name in Corpus.ls()}
        )
        self.lexica = util.Observable[Dict[str, Union[Lexicon, DefaultLexicon]]](
            {lexicon_name: Lexicon.load(lexicon_name) for lexicon_name in Lexicon.ls()}
        )
        self.current_report = util.Observable[Optional[str]](None)
        self.current_lexicon = util.Observable[Optional[str]](None)

        try:
            with open(constants.settings_path, "r") as settings_file:
                settings = toml.load(settings_file)
        except (FileNotFoundError, toml.TomlParsingError):
            settings = {
                "REDDIT_CLIENT_ID": None,
                "REDDIT_CLIENT_SECRET": None,
            }
        self.settings = util.Observable[Dict[str, Any]](settings)

        def persist_settings(settings: Dict[str, Any]) -> None:
            with open(constants.settings_path, "w") as settings_file:
                toml.dump(settings, settings_file)

        self.settings.subscribe(persist_settings, call=False)

        view = AppView(self, self, current_frame=self.current_frame)
        view.grid(row=0, column=0, sticky="nesw")

        tk.Tk.report_callback_exception = self.show_error

    def set_reddit_credentials(self, client_id: str, client_secret: str) -> None:
        """Sets the last-used Reddit credentials"""
        self.settings.set(
            {
                **self.settings.get(),
                "REDDIT_CLIENT_ID": client_id,
                "REDDIT_CLIENT_SECRET": client_secret,
            }
        )

    def set_current_frame(self, frame_name: str) -> None:
        """Sets the current frame"""
        self.current_frame.set(frame_name)

    def set_current_report(self, current_report: Optional[str]) -> None:
        """Sets the current report"""
        self.current_report.set(current_report)

    def set_current_lexicon(self, current_lexicon: Optional[str]) -> None:
        """Sets the current lexicon"""
        self.current_lexicon.set(current_lexicon)

    def create_report(
        self, report_name: str, corpus_name: str, lexicon_names: List[str]
    ) -> None:
        """Create a new report"""
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

    def create_lexicon(self, lexicon_name: str, words: List[Tuple[str, float]]) -> None:
        """Create a new lexicon"""
        lexicon = Lexicon(lexicon_name, words)

        # if a lexicon already exists with that name, update it
        if lexicon_name in self.lexica.get():
            self.lexica.get()[lexicon_name] = lexicon
        else:
            lexica: Dict[str, Union[DefaultLexicon, Lexicon]] = {
                **self.lexica.get(),
                lexicon_name: lexicon,
            }
            self.lexica.set(lexica)

    def add_corpus(self, corpus: Corpus) -> None:
        """Add a new corpus"""
        corpora = {
            **self.corpora.get(),
            corpus.name: corpus,
        }
        self.corpora.set(corpora)

    def on_corpus_complete(self) -> None:
        """Switch back to corpus list after download finishes"""
        if self.current_frame.get() == "CreateCorpusView":
            self.current_frame.set("CorpusListView")

    def delete_corpus(self, corpus_to_delete: str) -> None:
        """Delete a corpus"""
        corpora = self.corpora.get()

        if corpus_to_delete not in corpora:
            raise ValueError(f'Corpus "{corpus_to_delete}" doesn\'t exist!')

        self.corpora.set(
            {
                name: corpus
                for name, corpus in corpora.items()
                if name != corpus_to_delete
            }
        )
        corpora[corpus_to_delete].delete()

    def delete_report(self, report_to_delete: str) -> None:
        """Delete a report"""
        reports = self.reports.get()
        if self.current_report.get() == report_to_delete:
            self.set_current_report(None)

        if report_to_delete not in reports:
            raise ValueError('Report "{report_to_delete}" doesn\'t exist!')

        report = reports[report_to_delete]
        if report.in_progress.get():
            raise ValueError("That report is currently running!")

        self.reports.set(
            {
                name: report
                for name, report in reports.items()
                if name != report_to_delete
            }
        )
        reports[report_to_delete].delete()

    def delete_lexicon(self, lexicon_to_delete: str) -> None:
        """Delete a lexicon"""
        lexica = self.lexica.get()
        lexicon = lexica[lexicon_to_delete]
        if isinstance(lexicon, DefaultLexicon):
            return
        if self.current_lexicon.get() == lexicon_to_delete:
            self.set_current_lexicon(None)
        self.lexica.set(
            {
                name: lexicon
                for name, lexicon in lexica.items()
                if name != lexicon_to_delete
            }
        )
        lexicon.delete()

    @staticmethod
    def show_error(error: Exception) -> None:
        """Show an error dialog"""
        tk.messagebox.showerror("Error", f"Error: {error}")


def main() -> None:
    """Entry point"""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
