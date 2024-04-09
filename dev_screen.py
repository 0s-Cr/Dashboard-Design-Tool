from tkinter import *
from tkinter import filedialog
import os

from dash_icons import *

def dev_screen(loading=bool, filename=str):
    if loading:
        print("Load stuff here")
    master = Tk()
    master.title("Dashboard Designer - " + filename)
    master.after(0, lambda:master.state('zoomed'))

    pw = PanedWindow(orient='horizontal')
    pw.pack(fill='both', expand=True)

    # Sidebar for icons
    sidebar = Canvas(master, width=200, bg='#CCC', height=500, relief='sunken', borderwidth=2)
    mainarea = Canvas(master, bg='white', width=500, height=500)   
    sidebar.pack(expand=True, fill='both', side='left', anchor='nw')
    sidebar.config(highlightthickness=2, highlightbackground="black")
    sidebar_speedo = sidebar_icon(sidebar, mainarea, "Speed", 10, 10, 60, 60)
    pw.add(sidebar)

    # Main dev area
    mainarea.pack(expand=True, fill='both', side='right')
    pw.add(mainarea)

    master.mainloop()

if __name__ == "__main__":
    dev_screen(False, "No File")