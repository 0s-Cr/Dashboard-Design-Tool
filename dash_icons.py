import tkinter as tk
from tkinter import colorchooser
from config_window import *


def get_shape_from_type(canvas, type, has_label, x, y, width, height, color):
    # Returns an array of the shape type and a label (if has_label is True)
    # Designed to be reusable in both icon classes
    return_data = []
    match type:
        case "Speed":
            shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
            if has_label:
                label_text = "Speedometer"
                label = canvas.create_text(
                    x + width / 2, y + height + 10, text=label_text, width=80, anchor="center")
        case "RPM":
            shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
            if has_label:
                label_text = "Tachometer"
                label = canvas.create_text(
                    x + width / 2, y + height + 10, text=label_text, width=80, anchor="center")
        case "Fuel Temp":
            shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
            if has_label:
                label_text = "Fuel and Temperature"
                label = canvas.create_text(
                    x + width / 2, y + height + 10, text=label_text, width=80, anchor="center")
        case "Fuel":
            shape = canvas.create_rectangle(
                x, y, x + width, y + height/2, fill=color)
            if has_label:
                label_text = "Fuel Gague"
                label = canvas.create_text(
                    x + width / 2, y + height + 10, text=label_text, width=80, anchor="center")
        case "Temp":
            shape = canvas.create_rectangle(
                x, y, x + width, y + height/2, fill=color)
            if has_label:
                label_text = "Temperature Gague"
                label = canvas.create_text(
                    x + width / 2, y + height + 10, text=label_text, width=80, anchor="center")
        case "Volt Circle":
            shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
            if has_label:
                label_text = "Voltmeter"
                label = canvas.create_text(
                    x + width / 2, y + height + 10, text=label_text, width=80, anchor="center")
        case "Volt Digital":
            shape = canvas.create_rectangle(
                x, y, x + width, y + height/2, fill=color)
            if has_label:
                label_text = "Digital Voltmeter"
                label = canvas.create_text(
                    x + width / 2, y + height + 10, text=label_text, width=80, anchor="center")
        case _:
            shape = canvas.create_oval(x, y, x + width, y + height, fill="red")
            if has_label:
                label_text = "ERROR"
                label = canvas.create_text(
                    x + width / 2, y + height + 10, text=label_text, color="red", width=80, anchor="center")
    return_data.append(shape)
    if has_label:
        return_data.append(label)
    return return_data


class SidebarIcon:
    def __init__(self, manager, canvas, spawn_canvas, type, x, y, width=60, height=60, color="blue") -> None:
        self.manager = manager
        self.canvas = canvas
        self.spawn = spawn_canvas
        self.type = type
        shape_data = get_shape_from_type(
            self.canvas, self.type, True, x, y, width, height, color)
        self.shape = shape_data[0]
        self.label = shape_data[1]
        self.canvas.tag_bind(self.shape, "<Button-1>", self.spawn_object)

    def spawn_object(self, event):
        # Spawn a new instance of MovableIcon on the spawn canvas
        icon = MovableIcon(self.manager, self.spawn,
                           self.type, 10, 10, 50, 50, "blue")


class MovableIcon:
    def __init__(self, manager, canvas, type, x, y, width, height, color):
        self.manager = manager
        self.canvas = canvas
        self.type = type
        shape_data = get_shape_from_type(
            self.canvas, self.type, False, x, y, width, height, color)
        self.shape = shape_data[0]
        self.canvas.tag_bind(self.shape, "<Button-1>", self.on_press)
        self.canvas.tag_bind(self.shape, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.shape, "<ButtonRelease-1>", self.on_release)
        self.coords = self.canvas.coords(self.shape)
        self.prev_x = 0
        self.prev_y = 0
        self.resizing = False
        self.selected = False
        self.color = color
        self.labels = []
        self.prev_icon = [self.type, self.coords, self.color]
        self.id = self.manager.add_icon(
            self.shape, self.prev_icon)

    def on_press(self, event):
        # Actions when clicked with certain modifiers
        self.prev_x = event.x
        self.prev_y = event.y
        if event.state & 0x1:
            self.resizing = True
        elif event.state & 0x4 and self.type != "ERROR":
            config_window = ConfigWindow(self.canvas.master, self.canvas, self)
        else:
            self.resizing = False

    def on_drag(self, event):
        # Actions when dragged
        if self.resizing:
            width = event.x - self.canvas.coords(self.shape)[0]
            if self.type in ["Speed", "RPM", "Fuel Temp", "Voltmeter Gague"]:
                height = width
            else:
                height = event.y - self.canvas.coords(self.shape)[1]
            self.canvas.coords(self.shape, self.canvas.coords(self.shape)[0], self.canvas.coords(self.shape)[1],
                               self.canvas.coords(self.shape)[0] + width, self.canvas.coords(self.shape)[1] + height)
            self.canvas.coords(self.shape)
        else:
            new_x = event.x
            new_y = event.y
            self.canvas.move(self.shape, new_x - self.prev_x,
                             new_y - self.prev_y)
            self.prev_x = new_x
            self.prev_y = new_y
            self.coords = self.canvas.coords(self.shape)

    def on_release(self, event):
        self.resizing = False
        self.update_shape()

    def change_color(self, color):
        self.canvas.itemconfig(self.shape, fill=color)
        self.color = color
        self.update_shape()

    def change_pos(self, x, y, w, h):
        self.canvas.coords(self.shape, x, y, x + w, y + h)
        self.update_shape()

    def update_shape(self):
        self.manager.add_to_undo(self.id, self.prev_icon)
        new_icon = [self.type, self.coords,
                    self.canvas.itemcget(self.shape, "fill")]
        self.prev_icon = new_icon
        self.manager.update_icon(self.id, new_icon)
