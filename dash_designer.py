from tkinter import *
import tkinter as tk
from tkinter import filedialog
import os
from dev_screen import *

master = Tk()
master.title("Dashboard Designer")
master.geometry("750x500")
global filename
filename = ""

def create_files():
	filename = filedialog.asksaveasfilename(initialdir = os.path.dirname(os.path.realpath(__file__)),
										title = "Select a File",
										filetypes = (("Text files",
														"*.txt*"),
													("all files",
														"*.*")))
	return filename
	
def open_files():
	filename = filedialog.askopenfilename(initialdir = os.path.dirname(os.path.realpath(__file__)),
										title = "Select a File",
										filetypes = (("Text files",
														"*.txt*"),
													("all files",
														"*.*")))

def new_project():
	filename = create_files()
	print(filename)
	master.destroy()
	dev_screen(False, filename)
	

def open_project():
	filename = open_files()
	print(filename)
	master.destroy()
	dev_screen(True, filename)

title_label = Label(master, text="Dashboard Designer", width= 100, height=4)
new_button = Button(master, text="New Project", width=25, command=new_project)
existing_button = Button(master, text="Open Existing", width=25, command=open_files)
title_label.pack(), new_button.pack(), existing_button.pack()
master.mainloop()