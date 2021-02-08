import tkinter as tk
import buttons


class Dashboard(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller
        self.configure(bg="#ffffff")

        # top_navbar
        top_frame = tk.Frame(self)
        top_frame.configure(bg="#f2f3f4")
        top_frame.pack_propagate(False)

        # top_navbar buttons
        download_button = buttons.Buttons(
            self,
            lambda: printme(),
            "Download New Data",
            "PingFang TC",
            self.controller.main_color,
            self.controller.highlight_color,
        )
        download_button.configure(padx=10, pady=10)

        create_report_button = buttons.Buttons(
            self,
            lambda: controller.show_frame("CreateReportForm"),
            "Create New Report",
            "PingFang TC",
            self.controller.main_color,
            self.controller.highlight_color,
        )
        create_report_button.configure(padx=10, pady=10)

        lexicon_button = buttons.Buttons(
            self,
            lambda: printme(),
            "Create New Lexicon",
            "PingFang TC",
            self.controller.main_color,
            self.controller.highlight_color,
        )
        lexicon_button.configure(padx=10, pady=10)

        top_frame.grid(row=0, column=1, columnspan=4)
        download_button.grid(row=0, column=1)
        create_report_button.grid(row=0, column=2)
        lexicon_button.grid(row=0, column=3)


def printme():
    print(1)
