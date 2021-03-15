import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import font
import pognlp.view.theme as theme
import pognlp.view.common as common
from pognlp.model.corpus import Corpus, RedditCorpus
from pognlp.model.lexicon import Lexicon


class CreateLexiconView(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller
        self.configure(bg=theme.background_color_accent)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # labels
        self.name_label = common.Label(self, text="Name")
        self.name_label.grid(column=0, row=0, rowspan=1, sticky="sew")
        self.words_label = common.Label(self, text="Words")
        self.words_label.grid(column=0, row=1, rowspan=1, sticky="new")

        self.name_listbox = common.Entry(self)
        self.name_listbox.grid(column=1, row=0, sticky="nsew")

        self.words_listbox = tk.Text(self)
        self.words_listbox.grid(column=1, row=1, sticky="nsew")


        # button
        bottom_frame = tk.Frame(self)
        bottom_frame.configure(bg=theme.background_color_accent)
        bottom_frame.grid(column=0, columnspan=2, sticky="nesw")
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(2, weight=1)

        report_params_button = common.Button(
            bottom_frame,
            command=self.create_lexicon,
            text="Confirm Selections",
        )
        self.controller.current_frame.subscribe(self.update_info)
        report_params_button.grid(column=1, row=0, sticky="ns")

        report_params_button.configure(padx=10, pady=5)
    def create_lexicon(self):
        name = self.name_listbox.get()
        if not name:
            messagebox.showerror("Error", "Please enter a name.")
            return
        word_text = self.words_listbox.get('1.0','end')
        word_set = word_text.split('\n')
        word_list = []
        try:
            for word in word_set:
                if word != '':
                    word_split = word.split(';')
                    word_list.append((word_split[0],float(word_split[1])))
        except IndexError as e:
            tk.messagebox.showerror("Error","Each line must be a semicolon-separated word-number pair.")
            return
        except ValueError as e:
            tk.messagebox.showerror("Error","Each line must be a semicolon-separated word-number pair.")
            return
        self.controller.create_lexicon(name,word_list)
        self.name_listbox.delete(0,tk.END)
        self.words_listbox.delete('1.0','end')
        self.controller.set_current_lexicon(None)
        self.controller.set_current_frame("ReportView")

    def update_info(self,data):
        self.name_listbox.delete(0,tk.END)
        self.words_listbox.delete('1.0','end')
        if self.controller.current_lexicon.get() != None:
            lexicon = self.controller.lexica.get()[self.controller.current_lexicon.get()]
            self.name_listbox.insert(0,lexicon.name)
            word_text = ""
            for word in lexicon.words:
                word_text = word_text + word[0] + ";" + str(word[1]) + "\n"
            self.words_listbox.insert('1.0',word_text)
