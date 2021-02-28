import tkinter as tk

import pognlp.view.theme as theme
import pognlp.view.common as common


class LexicaListbox(tk.Listbox):
    def __init__(self, master, text, **kw):
        tk.Listbox.__init__(
            self,
            master=master,
            relief="flat",
            height=5,
            borderwidth=0,
            fg="#000000",
            bg=theme.background_color_accent,
            bd=0,
            width=100,
            exportselection=0,
            font=f.Font(family="Shree Devanagari 714", size=15),
            **kw,
        )
        # load lexica data
        self.insert(0, f"  {text}")

        self.bind(
            "<<ListboxSelect>>", lambda _: print(self.get(0))
        )  # open lexica for editing


class LexicaListView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=theme.background_color)

        self.report_names = frozenset()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(self)
        # self.listbox.grid(column=0, row=0, sticky="nesw")

        scrollbar = tk.Scrollbar(self)
        scrollbar.grid(column=2, row=0, sticky="ns")

        # for values in range(100):
        #     self.listbox.insert(tk.END, values)

        self.listbox.config(yscrollcommand=scrollbar.set)

        scrollbar.config(command=self.listbox.yview)

        self.controller.reports.subscribe(self.update_listbox)

    def update_listbox(self, lexicas):
        new_lexica_names = frozenset(lexica.name for lexica in lexicas)
        if self.lexica_names == new_lexica_names:
            return

        self.lexica_names = new_lexica_names

        # self.listbox.delete(0, tk.END)
        x = 0
        for lexica_name in self.lexica_names:
            # self.listbox.insert(tk.END, report_name)
            list_item = LexicaListbox(master=self, text=lexica_name)
            list_item.grid(column=0, row=x, sticky="nesw")
            delete_button = common.button(
                master=self, command=delete_lexica(lexica_name), text="Delete"
            )
            delete_button.grid(column=1, row=x)
            x = x + 1


def delete_lexica(name):
    lexica_name = name
    return lambda: delete_lexica2(lexica_name)


def delete_lexica2(report_name):
    print(1)
    # remove lexica from list


class LexicaView(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller
        self.configure(bg=theme.background_color)

        # top_navbar
        # top_frame = tk.Frame(self)
        # top_frame.configure(bg="#f2f3f4")
        # top_frame.grid(column=0, row=0)
