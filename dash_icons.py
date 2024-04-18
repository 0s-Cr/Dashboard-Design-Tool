import tkinter as tk
from tkinter import colorchooser
from config_window import *
global icon_list
icon_list = []

def get_icon_list():
    return icon_list
    

class SidebarIcon:
    def __init__(self, canvas, spawn_canvas, type, x, y, width=60, height=60, color="blue") -> None:
        self.canvas = canvas
        self.spawn = spawn_canvas
        self.type = type
        self.shape = tk.Canvas(canvas, width=width, height=height, bg='white', highlightthickness=0)
        match type:
            case "Speed":
                self.shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
                self.label_text = "Speedometer"
                self.label = canvas.create_text(x + width / 2, y + height + 10, text=self.label_text, width=80, anchor="center")
            case "RPM":
                self.shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
                self.label_text = "Tachometer"
                self.label = canvas.create_text(x + width / 2, y + height + 10, text=self.label_text, width=80, anchor="center")
            case "Fuel Temp":
                self.shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
                self.label_text = "Fuel and Temperature"
                self.label = canvas.create_text(x + width / 2, y + height + 10, text=self.label_text, width=80, anchor="center")
            case "Fuel":
                self.shape = canvas.create_rectangle(x, y, x + width, y + height/2, fill=color)
                self.label_text = "Fuel Gague"
                self.label = canvas.create_text(x + width / 2, y + height + 10, text=self.label_text, width=80, anchor="center")
            case "Temp":
                self.shape = canvas.create_rectangle(x, y, x + width, y + height/2, fill=color)
                self.label_text = "Temperature Gague"
                self.label = canvas.create_text(x + width / 2, y + height + 10, text=self.label_text, width=80, anchor="center")
            case "Volt Circle":
                self.shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
                self.label_text = "Voltmeter Gague"
                self.label = canvas.create_text(x + width / 2, y + height + 10, text=self.label_text, width=80, anchor="center")
            case "Volt Linear":
                self.shape = canvas.create_rectangle(x, y, x + width, y + height/2, fill=color)
                self.label_text = "Linear Voltmeter"
                self.label = canvas.create_text(x + width / 2, y + height + 10, text=self.label_text, width=80, anchor="center")
            case _:
                self.shape = canvas.create_oval(x, y, x + width, y + height, fill="red")
                self.label_text = "ERROR"
                self.label = canvas.create_text(x + width / 2, y + height + 10, text=self.label_text, color="red", width=80, anchor="center")
        self.canvas.tag_bind(self.shape, "<Button-1>", self.spawn_object)

    def spawn_object(self, event):
        #x, y = self.canvas.coords(self.shape)[:2]  # Get the top-left corner coordinates of the miniature icon
        icon = MovableIcon(self.spawn, self.type, 10, 10, 50, 50)  # Spawn a new instance of MovableIcon at the same position


class MovableIcon:
    def __init__(self, canvas, type, x, y, width, height, color="blue"):
        self.canvas = canvas
        self.type = type
        match type:
            case "Speed":
                self.shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
            case "RPM":
                self.shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
            case "Fuel Temp":
                self.shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
            case "Fuel":
                self.shape = canvas.create_rectangle(x, y, x+ width, y + height, fill= color)
            case "Temp":
                self.shape = canvas.create_rectangle(x, y, x+ width, y + height, fill= color)
            case "Volt Circle":
                self.shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
            case "Volt Linear":
                self.shape = canvas.create_rectangle(x, y, x+ width, y + height, fill= color)
            case _:
                self.shape = canvas.create_rectangle(x, y, x + width, y + height, fill="red")
        self.canvas.tag_bind(self.shape, "<Button-1>", self.on_press)
        self.canvas.tag_bind(self.shape, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.shape, "<ButtonRelease-1>", self.on_release)
        self.prev_x = 0
        self.prev_y = 0
        self.resizing = False

    def on_press(self, event):
        self.prev_x = event.x
        self.prev_y = event.y
        if event.state & 0x1:
            self.resizing = True
        elif event.state & 0x4 and self.type != "ERROR":
            config_window = ConfigWindow(self.canvas.master, self)
        else:
            self.resizing = False

    def on_drag(self, event):
        if self.resizing:
            width = event.x - self.canvas.coords(self.shape)[0]
            if self.type in ["Speed", "RPM", "Fuel Temp", "Voltmeter Gague"]:
                height = width
            else:
                height = event.y - self.canvas.coords(self.shape)[1]
            self.canvas.coords(self.shape, self.canvas.coords(self.shape)[0], self.canvas.coords(self.shape)[1],
                               self.canvas.coords(self.shape)[0] + width, self.canvas.coords(self.shape)[1] + height)
        else:
            new_x = event.x
            new_y = event.y
            self.canvas.move(self.shape, new_x - self.prev_x, new_y - self.prev_y)
            self.prev_x = new_x
            self.prev_y = new_y

    def on_release(self, event):
        self.resizing = False
        
    def change_colour(self, colour):
        self.canvas.itemconfig(self.shape, fill=colour)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Resizable Icon")

    canvas = tk.Canvas(root, width=400, height=300, bg="white")
    canvas.pack()

    # Create a miniature icon at position (10, 10)
    miniature_icon = SidebarIcon(canvas, canvas, "Speed", 10, 10)

    root.mainloop()