import tkinter as tk


class Navbar():
    def __init__(self, controller, x, y):
        self.controller = controller 
        self.x = x * .15
        self.y = y
        self.frame = tk.Frame(controller, width=self.x, height=self.y)
        self.frame.configure(bg="#30009C")

        #this makes it so the frame won't shrink to fit the buttons
        self.frame.pack_propagate(False)


   
