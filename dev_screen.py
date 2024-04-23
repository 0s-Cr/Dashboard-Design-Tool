from tkinter import *

from dash_icons import *
from dev_utils import *
from file_managment import *
from icon_manager import *
from dash_sim import *

global filename


def update_title_save(master, dev_area):
    filename = save_dash(True, None, dev_area)
    master.title("Dashboard Designer - " + filename)


def open_devscreen(master, manager, canvas):
    filename = load_files(False, True, None, manager, canvas)
    master.destroy()
    dev_screen(True, filename)


def go_to_sim(master, filename, manager, dev_area):
    sim_screen(filename, manager, dev_area.get_coords())


def new_project(master):
    master.destroy()
    dev_screen(False, "No File")


def dev_screen(loading=bool, filename=str):
    master = Tk()
    master.title("Dashboard Designer - " + filename)
    master.after(0, lambda: master.state('zoomed'))

    pw = PanedWindow(orient='horizontal')
    pw.pack(fill='both', expand=True)

    # Sidebar for icons
    sidebar = Canvas(master, width=150, bg='#CCC', height=500,
                     relief='sunken', borderwidth=2)

    mainarea = Canvas(master, bg='grey', width=500, height=500)

    # Icon manager
    manager = IconManager(mainarea)

    # Main dev area
    dev_area = DevArea(manager, mainarea, 4, 100, 750, 500)

    # Menu bar
    menubar = Menu(master)
    # File menu
    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="New", command=lambda: new_project(master))
    file_menu.add_command(
        label="Open", command=lambda: open_devscreen(master, manager, mainarea))
    if filename == "No File":
        file_menu.add_command(label="Save", command=None, foreground="grey")
    else:
        file_menu.add_command(
            label="Save", command=lambda: save_dash(False, filename, dev_area))
    file_menu.add_command(label="Save As...",
                          command=lambda: update_title_save(master, dev_area))
    file_menu.add_separator()
    file_menu.add_command(label="Simulate", command=lambda: go_to_sim(
        master, filename, manager, dev_area))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=quit)
    menubar.add_cascade(label="File", menu=file_menu)
    # Edit menu
    edit_menu = Menu(menubar, tearoff=0)
    master.config(menu=menubar)
    edit_menu.add_command(label="Undo", command=lambda: manager.undo_redo("z"))
    edit_menu.add_command(label="Redo", command=lambda: manager.undo_redo("y"))
    menubar.add_cascade(label="Edit", menu=edit_menu)

    # Sidebar
    sidebar.pack(expand=True, fill='both', side='left', anchor='nw')
    sidebar.config(highlightthickness=2, highlightbackground="black")
    '''Types are:
    - Speed
    - RPM
    - Fuel Temp
    - Fuel
    - Temp
    - Volt Circle
    - Volt Digital
    Any other entry will result in an ERROR figure (red circle which spawns a red square)'''
    sidebar_icons_list = [
        SidebarIcon(manager, sidebar, mainarea, "Speed", 10, 10),
        SidebarIcon(manager, sidebar, mainarea, "RPM", 90, 10),
        SidebarIcon(manager, sidebar, mainarea, "Fuel", 10, 120),
        SidebarIcon(manager, sidebar, mainarea, "Temp", 90, 120),
        SidebarIcon(manager, sidebar, mainarea, "Volt Circle", 10, 240),
        SidebarIcon(manager, sidebar, mainarea, "Volt Digital", 90, 240),
        SidebarIcon(manager, sidebar, mainarea, "Fuel Dial", 10, 360)
    ]
    pw.add(sidebar)

    mainarea.pack(expand=True, fill='both', side='right')
    pw.add(mainarea)

    # Input detection
    master.bind("<Control-z>", manager.undo_redo)
    master.bind("<Control-y>", manager.undo_redo)
    master.bind("<Control-l>", manager.toggle_labels)

    if loading:
        load_files(loading, True, filename, manager, mainarea)

    master.mainloop()


if __name__ == "__main__":
    dev_screen(False, "No File")
