from tkinter import *
from tkinter import filedialog
import os

from dash_icons import *

# TODO make this work 
def on_sidebar_resize(event, sidebar):
    sidebar_width = event.width
    if sidebar_width < 80:
        sidebar.config(width=80)
        sidebar.after(1, lambda: sidebar.config(width=80))

def dev_screen(loading=bool, filename=str):
    if loading:
        print("Load stuff here")
    master = Tk()
    master.title("Dashboard Designer - " + filename)
    master.after(0, lambda:master.state('zoomed'))

    pw = PanedWindow(orient='horizontal')
    pw.pack(fill='both', expand=True)

    # Sidebar for icons
    sidebar = Canvas(master, width=150, bg='#CCC', height=500, relief='sunken', borderwidth=2)
    mainarea = Canvas(master, bg='white', width=500, height=500)   
    sidebar.pack(expand=True, fill='both', side='left', anchor='nw')
    sidebar.config(highlightthickness=2, highlightbackground="black")
    sidebar.bind("<Configure>", lambda event: on_sidebar_resize(event, sidebar))
    '''Types are:
    - Speed
    - RPM
    - Fuel Temp
    - Fuel
    - Temp
    - Volt Circle
    - Volt Linear
    Any other entry will result in an ERROR figure (red circle which spawns a red square)'''
    sidebar_icons_list = [
        SidebarIcon(sidebar, mainarea, "Speed", 10, 10),
        SidebarIcon(sidebar, mainarea, "RPM", 90, 10),
        SidebarIcon(sidebar, mainarea, "Fuel Temp", 10, 120),
        SidebarIcon(sidebar, mainarea, "Fuel", 90, 120),
        SidebarIcon(sidebar, mainarea, "Temp", 10, 240),
        SidebarIcon(sidebar, mainarea, "Volt Circle", 90, 240),
        SidebarIcon(sidebar, mainarea, "Volt Linear", 10, 360)
    ]
    pw.add(sidebar)

    # Main dev area
    mainarea.pack(expand=True, fill='both', side='right')
    pw.add(mainarea)

    master.mainloop()

if __name__ == "__main__":
    dev_screen(False, "No File")