import tkinter as tk
import tkinter.font as font
import sys
import side_listbox
import dashboard as dash
import create_report_form as form1
import dictionary_dash as dash2
import report_dash as dash3

class App(tk.Tk):
    #initializes the App 
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.grid(row=0, column=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_configure(rowspan=10, columnspan=10)
        
        self.frames = {}
        #this will contain all frames so they will be available
        #to raise
        for F in (dash.Dashboard, form1.CreateReportForm, dash2.DictionaryDashboard,
        dash3.ReportDashboard):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Dashboard")  

    #function to raise a specific frame
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

  

#starts the mainloop
if __name__=="__main__":
    app = App() 
    app.mainloop()



