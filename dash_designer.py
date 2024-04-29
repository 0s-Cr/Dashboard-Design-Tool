from dev_screen import *

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


def skip_to_dev(filename):
    dev_screen(True, filename)


title_label = Label(master, text="Dashboard Designer", height=4, font=(
    "Helvetica", 32, "bold italic"), fg="#1f2a44")
image = tk.PhotoImage(file="images/york_words.png").subsample(3)
image_label = Label(master, image=image)
image_label.pack()
new_button = Button(master, text="New Project",
                    width=25, command=new_project)
existing_button = Button(master, text="Open Existing",
                         width=25, command=open_project)
title_label.pack(), new_button.pack(), existing_button.pack()
master.mainloop()
