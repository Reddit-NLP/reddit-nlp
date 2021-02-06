import tkinter as tk
import buttons
import side_listbox

main_color = "#30009C"
class SideNavbar():
    def __init__(self, controller, x, y):
        self.controller = controller 
        self.x = x * .15
        self.y = y

        self.x2 = x * .15
        self.y2 = y * .15

        self.frame = tk.Frame(controller, width=self.x, height=self.y)
        self.frame.configure(bg=main_color)
        #this makes it so the frame won't shrink to fit 
        self.frame.pack_propagate(False)

        self.frame2 = tk.Frame(controller, width=self.x2, height=self.y2)
        self.frame2.configure(bg=main_color)
        self.frame2.pack_propagate(False)


        #using listboxes was the best way to get the same visual
        #effect across all platforms given macs dont let tkinter
        #change the background color 
        self.side_list1 = side_listbox.SideListbox(self.frame, bg=main_color)
        self.side_list1.pack()
        self.side_list1.insert(0, "Home")

        self.side_list2 = self.side_list1 = side_listbox.SideListbox(self.frame, bg=main_color)
        self.side_list2.pack()
        self.side_list2.insert(0, "Dictionary")

        self.side_list3 = self.side_list1 = side_listbox.SideListbox(self.frame, bg=main_color)
        self.side_list3.pack()
        self.side_list3.insert(0, "Reports")