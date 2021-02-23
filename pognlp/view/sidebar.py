import tkinter as tk
import tkinter.font as f

import pognlp.view.theme as theme


class SideListbox(tk.Listbox):
    def __init__(self, master, text, on_select, **kw):
        self.default_background = theme.main_color
        tk.Listbox.__init__(
            self,
            master=master,
            relief="flat",
            height=0,  # height=0 sets it so the listboxes are wrapped around their items
            borderwidth=0,
            fg=theme.background_color_accent,
            bg=self.default_background,
            bd=0,
            width=13,
            exportselection=0,
            font=f.Font(family="Shree Devanagari 714", size=15),
            **kw,
        )

        self.insert(0, f"  {text}")

        self.bind("<<ListboxSelect>>", on_select)

        # binds these functions on mouse enter, motion, or leave
        self.bind("<Enter>", self.snap_highlight_to_mouse)
        self.bind("<Motion>", self.snap_highlight_to_mouse)
        self.bind("<Leave>", self.unhighlight)

    # what happens on hover if the listbox is >1 item then this
    # method will not work correctly with its partner
    def snap_highlight_to_mouse(self, event):
        self.selection_clear(0, tk.END)
        self.itemconfig(
            self.nearest(event.y), bg=theme.highlight_color, fg=self.default_background
        )

    # what happens on leave
    def unhighlight(self, event):
        self.selection_clear(0, tk.END)
        self.itemconfig(
            self.nearest(event.y),
            bg=self.default_background,
            fg=theme.background_color_accent,
        )


class Sidebar(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller

        self.configure(bg=theme.main_color)

        self.grid_rowconfigure(0, minsize=100)
        self.grid_rowconfigure(1, minsize=150)
        self.grid_rowconfigure(2, minsize=150)
        self.grid_rowconfigure(3, minsize=150)

        # items for navbar
        home_item = SideListbox(
            master=self,
            text="Home",
            on_select=lambda _: controller.set_current_frame("HomeView"),
        )
        home_item.grid(column=0, row=1)

        lexica_item = SideListbox(
            master=self,
            text="Lexica",
            on_select=lambda _: controller.set_current_frame("LexicaView"),
        )
        lexica_item.grid(column=0, row=2)

        reports_item = SideListbox(
            master=self,
            text="Reports",
            on_select=lambda _: controller.set_current_frame("ReportListView"),
        )
        reports_item.grid(column=0, row=3)


#         dictionary_item = SideListbox(
#             self, bg=theme.main_color, width=13, exportselection=0
#         )
#         dictionary_item.grid(column=0, row=2)
#         dictionary_item.insert(0, "  Dictionaries")
#         dictionary_item.bind(
#             "<<ListboxSelect>>", lambda x: controller.show_frame("DictionaryDashboard")
#         )

#         reports_item = SideListbox(
#             self, bg=theme.main_color, width=13, exportselection=0
#         )
#         reports_item.grid(column=0, row=3)
#         reports_item.insert(0, "  Reports")
#         reports_item.bind(
#             "<<ListboxSelect>>", lambda x: controller.show_frame("ReportDashboard")
#         )
