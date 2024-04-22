from tkinter import filedialog
import os
import ast
from dash_icons import *


def create_files():
    filename = filedialog.asksaveasfilename(initialdir=os.path.dirname(os.path.realpath(__file__)),
                                            title="Select a File",
                                            filetypes=(("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
    if not filename.endswith(".txt"):
        filename = filename + ".txt"
    return filename


def open_files():
    filename = filedialog.askopenfilename(initialdir=os.path.dirname(os.path.realpath(__file__)),
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.txt*"),
                                                     ("all files",
                                                      "*.*")))
    return filename


def save_dash(save_as, filename, dev_area):
    if save_as:
        filename = create_files()
    f = open(filename, "w")
    f.write(f"{dev_area.check_for_shapes()}")
    f.close()
    return filename


def load_files(loading, dev, filename, manager, canvas):
    if not loading:
        filename = open_files()
    try:
        f = open(filename, "r")
        contents = f.read()
        data = ast.literal_eval(contents)
        if isinstance(data, list):
            for i in data:
                if len(i[1]) == 3:
                    width = abs(i[1][1][0] - i[1][1][2])
                    height = abs(i[1][1][1] - i[1][1][3])
                    if dev:
                        icon = MovableIcon(
                            manager, canvas, i[1][0], i[1][1][0], i[1][1][1], width, height, i[1][2])
                else:
                    if dev:
                        icon = MovableIcon(
                            manager, canvas, i[1][0], i[1][1][0], i[1][1][1], i[1][2][0], i[1][2][1], i[1][3])
        else:
            print("Error loading")
        f.close()
        return filename
    except FileNotFoundError:
        return "FILE ERROR"
