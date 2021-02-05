import tkinter as tk
import app
import buttons as b


#Button class def __init__(self, master, text, font, color, active_color, function):
class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller 
        self.configure(bg='#f2f3f4')

        button_font1 = tk.font.Font(family="PT Sand", size=20)
        exit_button = b.Buttons(self.controller, "Exit", button_font1, "#7F39FB", "#FB3552", None)
        exit_button.pack()


        