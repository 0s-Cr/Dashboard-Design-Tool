from tkinter import *
from dev_screen import *
from dev_utils import *

master = Tk()
master.title("Dashboard Designer")
master.geometry("750x500")


def new_project():
    filename = create_files()
    if filename:
        master.destroy()
        dev_screen(False, filename)


def open_project():
    filename = open_files()
    if filename:
        master.destroy()
        dev_screen(True, filename)


title_label = Label(master, text="Dashboard Designer", width=100, height=4)
new_button = Button(master, text="New Project", width=25, command=new_project)
existing_button = Button(master, text="Open Existing",
                         width=25, command=open_project)
title_label.pack(), new_button.pack(), existing_button.pack()
master.mainloop()
