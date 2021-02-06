import tkinter as tk
import tkinter as tk 
from tkinter import font
class CreateReportForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller 

        self.x = 800
        self.y = 500

    
        self.configure(bg="red")
        controller.geometry("%dx%d" % (self.x, self.y))





        self.grid(column=0, row=0, columnspan=100, rowspan=100)