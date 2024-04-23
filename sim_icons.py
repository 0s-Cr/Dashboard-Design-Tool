from tkinter import *
from config_window import *
import math


def get_default_values(type):
    match type:
        case "Speed":
            return [0, 160, 10, "Dial"]
        case "RPM":
            return [0, 8, 1, "Dial"]
        case "Fuel Dial":
            return [0, 100, 25, "Dial"]
        case "Volt Circle":
            return [570, 690, 10, "Dial"]
        case _:
            return [0, 240, 20, "Dial"]


class SimIcon:
    def __init__(self, manager, canvas, type, x, y, width, height):
        self.manager = manager
        self.canvas = canvas
        self.type = type
        min_value, max_value, increment, shape = get_default_values(self.type)
        self.shape = Dial(self.canvas, self.type, min_value,
                          max_value, x, y, width, height, increment).shape


class Dial():
    def __init__(self, canvas, type, min_value, max_value, x, y, width, height, increment):
        self.canvas = canvas
        self.shape = None
        self.width = width
        self.height = height
        self.type = type
        self.start_angle = 210
        self.radius = min(self.width, self.height) / 2 - 10
        self.center = (x + self.width / 2, y + self.height / 2)
        self.min_value = min_value
        self.max_value = max_value
        self.needle = None
        self.increment = increment
        self.labels = []
        self.create_dial()
        self.update_needle(60)

    def create_dial(self):
        self.shape = self.canvas.create_oval(
            self.center[0] - self.radius,
            self.center[1] - self.radius,
            self.center[0] + self.radius,
            self.center[1] + self.radius,
            outline="black", width=2,
            fill="light grey")
        self.canvas.tag_bind(self.shape, "<Button-1>", self.on_press)
        step = int(
            round(240 / ((self.max_value-self.min_value) / self.increment)))
        number = self.min_value
        for angle in range(self.start_angle, self.start_angle - 241, -step):
            radian = math.radians(angle)
            x = self.center[0] + self.radius * 0.925 * math.cos(radian)
            y = self.center[1] - self.radius * 0.925 * math.sin(radian)
            label = self.canvas.create_text(
                x, y, text=str(number), fill="black")
            self.labels.append(label)
            number += self.increment
        match self.type:
            case "Speed":
                add_text = "MPH"
            case "RPM":
                add_text = "x1000 RPM"
            case "Fuel Dial":
                add_text = "Fuel %"
            case "Volt Circle":
                add_text = "Volts"
            case _:
                add_text = ""
        self.canvas.create_text(
            self.center[0], self.center[1] - self.radius * 0.925 * math.sin(radian), text=add_text, fill="black")

    def update_needle(self, target_val):
        if self.needle:
            self.delete(self.needle)
        if target_val == 0:
            angle = self.start_angle
        else:
            target_pos = target_val / self.max_value
            angle = self.start_angle - target_pos * 240
        radian = math.radians(angle)
        x = self.center[0] + self.radius * 0.85 * math.cos(radian)
        y = self.center[1] - self.radius * 0.85 * math.sin(radian)
        self.needle = self.canvas.create_line(
            self.center[0], self.center[1], x, y, fill="red", width=2
        )

    def update_labels(self, min_value, max_value, increment):
        self.min_value, self.max_value, self.increment = min_value, max_value, increment
        if self.labels != []:
            for label in self.labels:
                self.canvas.delete(label)
            self.labels.clear()
        step = int(
            round(240 / ((self.max_value-self.min_value) / self.increment)))
        number = self.min_value
        for angle in range(self.start_angle, self.start_angle - 241, -step):
            radian = math.radians(angle)
            x = self.center[0] + self.radius * 0.925 * math.cos(radian)
            y = self.center[1] - self.radius * 0.925 * math.sin(radian)
            label = self.canvas.create_text(
                x, y, text=str(number), fill="black")
            self.labels.append(label)
            number += self.increment

    def on_press(self, event):
        # Actions when clicked with certain modifiers
        if event.state & 0x4 and self.type != "ERROR":
            config_window = SimConfigWindow(
                self.canvas.master, self.canvas, self)


if __name__ == "__main__":
    root = Tk()
    root.title("Fuel Example")
    root.geometry("500x500")

    canvas = Canvas(root, width=500, height=500)
    canvas.pack()

    speedometer = SimIcon(None, canvas, "Fuel", 100,
                          100, width=300, height=300)

    speed_label = Label(root, text="Fuel: 0 mph")
    speed_label.pack()

    # Example usage: Update the speedometer speed

    root.mainloop()
