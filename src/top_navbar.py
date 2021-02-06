import tkinter as tk


class TopNavbar():
    def __init__(self, controller, x, y):
        self.controller = controller 
        self.x = x * .85
        self.y = y * .15
        self.frame = tk.Frame(controller, width=self.x, height=self.y)
        self.frame.configure(bg="#f2f3f4")

        #this makes it so the frame won't shrink to fit the buttons
        self.frame.pack_propagate(False)

