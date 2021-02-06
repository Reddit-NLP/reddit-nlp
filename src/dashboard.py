import tkinter as tk
import app
import buttons
import side_navbar
import top_navbar
import app
import side_listbox


class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        self.parent=parent

        #change this to change window dimensions
        self.x = 800
        self.y = 500

        tk.Frame.__init__(self, parent)
        self.controller = controller 
        self.configure(bg="#000000")
        controller.geometry("%dx%d" % (self.x, self.y))
        
        #side navbar
        snavbar_frame = side_navbar.SideNavbar(controller, self.x, self.y)
        #top_navbar
        tnavbar_frame = top_navbar.TopNavbar(controller, self.x, self.y)




        """had to break the side navbar into two to account for the way
        tkinter organizes its grid placements"""
        snavbar_frame.frame2.grid(row=0, column=0)
        snavbar_frame.frame.grid(row=1, column=0)
        tnavbar_frame.frame.grid(row=0, column=1)
        
        

        