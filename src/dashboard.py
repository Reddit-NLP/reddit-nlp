import tkinter as tk
import app
import buttons
import side_listbox as listbox

main_color = "#30009C"
highlight_color = "#FB3552"

class Dashboard(tk.Frame):
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
        
        #top_navbar buttons
        download_button = buttons.Buttons(self, lambda: printme(), 
        "Download New Data", "PingFang TC", main_color, highlight_color)
        download_button.configure(padx=10, pady=10)

        create_report_button = buttons.Buttons(self, 
        lambda: controller.show_frame("CreateReportForm"), 
        "Create New Report", "PingFang TC", main_color, highlight_color)
        create_report_button.configure(padx=10, pady=10)
        
        lexicon_button = buttons.Buttons(self, lambda: printme() ,
        "Create New Lexicon", "PingFang TC", main_color, highlight_color)
        create_report_button.configure(padx=10, pady=10)

        #side navbar
        side_nav_width = self.x * .15

        side_frame = tk.Frame(self, width=side_nav_width, height=self.y)
        side_frame.configure(bg=main_color)
        side_frame2 = tk.Frame(self, width=side_nav_width, height=self.y * .15)
        side_frame2.configure(bg=main_color)


        #items for navbar
        home_item = listbox.SideListbox(self, bg=main_color, width=13)
        home_item.insert(0, "  Home")

        dictionary_item = listbox.SideListbox(self, bg=main_color, width=13)
        dictionary_item.insert(0, "  Dictionaries")

        reports_item = listbox.SideListbox(self, bg=main_color, width=13)
        reports_item.insert(0, "  Reports")



        side_frame.grid(row=1, column=0, rowspan=10)
        side_frame2.grid(row=0, column=0)
        home_item.grid(row=1, column=0)
        dictionary_item.grid(row=2, column=0)
        reports_item.grid(row=3, column=0)

        top_frame.grid(row=0, column=1, columnspan=4)
        download_button.grid(row=0, column=1)
        create_report_button.grid(row=0, column=2)
        lexicon_button.grid(row=0, column=3)
    

        


def printme():
    print(1)