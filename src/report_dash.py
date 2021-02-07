import tkinter as tk
import app
import buttons
import side_listbox as listbox

main_color = "#30009C"
highlight_color = "#FB3552"

class ReportDashboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.x = 800
        self.y = 500
        self.controller = controller 
        self.configure(bg="#ffffff")
       
        #top_navbar
        top_frame = tk.Frame(self, width=self.x, height=self.y * .15)
        top_frame.configure(bg="#f2f3f4")
        top_frame.pack_propagate(False)
        

        #side navbar
        side_nav_width = self.x * .15

        side_frame = tk.Frame(self, width=side_nav_width, height=self.y)
        side_frame.configure(bg=main_color)
        side_frame2 = tk.Frame(self, width=side_nav_width, height=self.y * .15)
        side_frame2.configure(bg=main_color)


        #items for navbar
        home_item = listbox.SideListbox(self, bg=main_color, width=13, exportselection=0)
        home_item.insert(0, "  Home")
        home_item.bind('<<ListboxSelect>>', lambda x:controller.show_frame("Dashboard"))

        dictionary_item = listbox.SideListbox(self, bg=main_color, width=13, exportselection=0)
        dictionary_item.insert(0, "  Dictionaries")
        dictionary_item.bind('<<ListboxSelect>>', lambda x:controller.show_frame("DictionaryDashboard"))

        reports_item = listbox.SideListbox(self, bg=main_color, width=13, exportselection=0)
        reports_item.insert(0, "  Reports")
        reports_item.bind('<<ListboxSelect>>', lambda x:controller.show_frame("ReportDashboard"))


        side_frame.grid(row=1, column=0, rowspan=10)
        side_frame2.grid(row=0, column=0)
        home_item.grid(row=1, column=0)
        dictionary_item.grid(row=2, column=0)
        reports_item.grid(row=3, column=0)

        top_frame.grid(row=0, column=1, columnspan=4)
   