import tkinter as tk
import tkinter.font as f


class SideListbox(tk.Listbox):
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]

        # binds these functions on mouse enter, motion, or leave
        self.bind("<Enter>", self.snap_highlight_to_mouse)
        self.bind("<Motion>", self.snap_highlight_to_mouse)
        self.bind("<Leave>", self.unhighlight)
        self.font = f.Font(family="Shree Devanagari 714", size=15)

        # height=0 sets it so the listboxes are wrapped around their items
        self.config(fg="#f2f3f4", bd=0, font=self.font, height=0)

    # what happens on hover if the listbox is >1 item then this
    # method will not work correctly with its partner
    def snap_highlight_to_mouse(self, event):
        self.selection_clear(0, tk.END)
        self.itemconfig(self.nearest(event.y), bg="#FB3552", fg=self.defaultBackground)

    # what happens on leave
    def unhighlight(self, event):
        self.selection_clear(0, tk.END)
        self.itemconfig(self.nearest(event.y), bg=self.defaultBackground, fg="#f2f3f4")


class Sidebar(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller

        self.configure(bg="#000033")

        # items for navbar
        home_item = SideListbox(
            self, bg=self.controller.main_color, width=13, exportselection=0
        )
        home_item.grid(column=0, row=1)
        home_item.insert(0, "  Home")
        home_item.bind(
            "<<ListboxSelect>>", lambda x: controller.show_frame("Dashboard")
        )

        dictionary_item = SideListbox(
            self, bg=self.controller.main_color, width=13, exportselection=0
        )
        dictionary_item.grid(column=0, row=2)
        dictionary_item.insert(0, "  Dictionaries")
        dictionary_item.bind(
            "<<ListboxSelect>>", lambda x: controller.show_frame("DictionaryDashboard")
        )

        reports_item = SideListbox(
            self, bg=self.controller.main_color, width=13, exportselection=0
        )
        reports_item.grid(column=0, row=3)
        reports_item.insert(0, "  Reports")
        reports_item.bind(
            "<<ListboxSelect>>", lambda x: controller.show_frame("ReportDashboard")
        )
