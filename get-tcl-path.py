from tkinter import Tcl

print(Tcl().eval("join $::auto_path *").split("*")[0])
