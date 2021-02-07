import tkinter as tk
import tkinter.font as f
import app


class SideListbox(tk.Listbox):
    
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master = master, **kw)
        self.defaultBackground = self["background"]

        #binds these functions on mouse enter, motion, or leave
        self.bind("<Enter>", self.snap_highlight_to_mouse)
        self.bind("<Motion>", self.snap_highlight_to_mouse)
        self.bind("<Leave>", self.unhighlight)
        self.font = f.Font(family="Shree Devanagari 714", size=15)

        #height=0 sets it so the listboxes are wrapped around their items
        self.config(fg="#f2f3f4", bd=0, font=self.font, height=0)

    #what happens on hover if the listbox is >1 item then this 
    #method will not work correctly with its partner
    def snap_highlight_to_mouse(self, event):
        self.selection_clear(0, tk.END)
        self.itemconfig(self.nearest(event.y), bg="#FB3552", fg=self.defaultBackground)

    #what happens on leave
    def unhighlight(self, event):
        self.selection_clear(0, tk.END)
        self.itemconfig(self.nearest(event.y), bg=self.defaultBackground, fg="#f2f3f4")
