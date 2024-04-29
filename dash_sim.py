from dev_screen import *
from file_management import *
from sim_manager import *


def on_exit(sim_manager, master):
    sim_manager.on_exit()
    master.destroy()


def sim_screen(filename, dev_coords):
    master = Tk()
    master.title("Dashboard Simulator - " + filename)
    master.after(0, lambda: master.state('zoomed'))
    master.grab_set()

    pw = PanedWindow(orient='horizontal')
    pw.pack(fill='both', expand=True)

    # Sidebar for icons
    sidebar = Canvas(master, width=150, height=500,
                     relief='sunken', borderwidth=2)
    tk.Label(sidebar, text="Motor Controller Errors").pack()
    selection_frame = tk.Frame(sidebar)
    selection_frame.pack()

    mainarea = Canvas(master, bg='grey', width=500, height=500)

    # Main sim area
    x1, y1, x2, y2 = dev_coords
    sim_area = mainarea.create_rectangle(x1, y1, x2, y2, fill="white")

    manager = SimManager(mainarea)
    manager.create_selections(selection_frame)

    Label(sidebar, text="Speed Percentage").pack()
    slider = Scale(sidebar, length=150, from_=0, to=100, orient=HORIZONTAL,
                   command=lambda value: manager.update_dials(0, value))
    slider.pack()

    Label(sidebar, text="RPM Percentage").pack()
    slider = Scale(sidebar, length=150, from_=0, to=100, orient=HORIZONTAL,
                   command=lambda value: manager.update_dials(1, value))
    slider.pack()

    Label(sidebar, text="Fuel Percentage").pack()
    slider = Scale(sidebar, length=150, from_=0, to=100, orient=HORIZONTAL,
                   command=lambda value: manager.update_dials(2, value))
    slider.pack()

    Label(sidebar, text="Voltage Percentage").pack()
    slider = Scale(sidebar, length=150, from_=0, to=100, orient=HORIZONTAL,
                   command=lambda value: manager.update_dials(3, value))
    slider.pack()

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
    master.protocol("WM_DELETE_WINDOW", lambda: on_exit(manager, master))

    master.mainloop()
