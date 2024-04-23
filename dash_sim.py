from tkinter import *
from dev_screen import *
from file_managment import *


def sim_screen(filename, manager, dev_coords):
    master = Tk()
    master.title("Dashboard Simulator - " + filename)
    master.after(0, lambda: master.state('zoomed'))
    master.grab_set()

    pw = PanedWindow(orient='horizontal')
    pw.pack(fill='both', expand=True)

    # Sidebar for icons
    sidebar = Canvas(master, width=150, bg='#CCC', height=500,
                     relief='sunken', borderwidth=2)

    mainarea = Canvas(master, bg='grey', width=500, height=500)

    # Main sim area
    x1, y1, x2, y2 = dev_coords
    sim_area = mainarea.create_rectangle(x1, y1, x2, y2, fill="white")

    # Menu bar
    menubar = Menu(master)
    # File menu
    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="Return", command=master.destroy)
    menubar.add_cascade(label="File", menu=file_menu)
    # Simulation menu
    sim_menu = Menu(menubar, tearoff=0)
    master.config(menu=menubar)
    menubar.add_cascade(label="Simulation", menu=sim_menu)

    # Sidebar
    sidebar.pack(expand=False, fill='both', side='left', anchor='nw')
    sidebar.config(highlightthickness=2, highlightbackground="black")
    pw.add(sidebar)

    mainarea.pack(expand=True, fill='both', side='right')
    pw.add(mainarea)

    load_files(True, False, filename, manager, mainarea)

    master.mainloop()
