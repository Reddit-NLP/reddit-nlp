import tkinter as tk
import tkinter.font as font
import sys
import dashboard as dash
import start as st

class App(tk.Tk):
    #initializes the App 
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        container = tk.Frame(self)
        
        self.frames = {}
        #this will contain all frames so they will be available
        #to raise
        for f in (dash.Dashboard, st.StartPage):
            frame_name = f.__name__
            frame = f(parent = container, controller = self)
            self.frames[frame_name] = frame

        self.show_frame("Dashboard")

    #function to raise a specific frame
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

#starts the mainloop
if __name__=="__main__":
    app = App()
    app.mainloop()

