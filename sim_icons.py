from tkinter import *
import can

from config_window import *
import math
import threading


def get_default_values(type):
    match type:
        case "Speed":
            return [0, 160, 10, "Dial", "Speed"]
        case "RPM":
            return [0, 8, 1, "Dial", "RPM"]
        case "Fuel Dial":
            return [0, 100, 25, "Dial", "Fuel"]
        case "Volt Circle":
            return [570, 690, 10, "Dial", "Voltage"]
        case "Gen Display":
            return [0, 0, 0, "Logger", "CAN_output"]
        case _:
            return [0, 0, 0, "Logger", None]


class SimIcon:
    def __init__(self, manager, canvas, type, x, y, width, height):
        self.manager = manager
        self.canvas = canvas
        self.type = type
        min_value, max_value, increment, shape, channel = get_default_values(
            self.type)
        match shape:
            case "Dial":
                self.shape = Dial(self.canvas, self.type, min_value,
                                  max_value, x, y, width, height, increment, channel)
            case "Logger":
                self.shape = DigitalDisplay(
                    self.canvas, self.type, x, y, width, height, channel)
        manager.add_icon(self)

    def kill_all(self):
        if hasattr(self.shape, "display_thread"):
            if self.shape.display_thread != None:
                self.shape.display_thread.join(5.0)


class Dial():
    def __init__(self, canvas, type, min_value, max_value, x, y, width, height, increment, channel):
        self.canvas = canvas
        self.shape = None
        self.channel = channel
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
        match self.type:
            case "Speed":
                self.add_text = "MPH"
            case "RPM":
                self.add_text = "x1000 RPM"
            case "Fuel Dial":
                self.add_text = "Fuel %"
            case "Volt Circle":
                self.add_text = "Volts"
            case _:
                self.add_text = ""
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
        label = self.canvas.create_text(
            self.center[0], self.center[1] - self.radius * 0.925 * math.sin(radian), text=self.add_text, fill="black")
        self.labels.append(label)

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
        label = self.canvas.create_text(
            self.center[0], self.center[1] - self.radius * 0.925 * math.sin(radian), text=self.add_text, fill="black")
        self.labels.append(label)

    def on_press(self, event):
        # Actions when clicked with certain modifiers
        if event.state & 0x4 and self.type != "ERROR":
            config_window = SimConfigWindow(
                self.canvas.master, self.canvas, self)


class DigitalDisplay():
    def __init__(self, canvas, type, x, y, width, height, channel):
        self.channel = channel
        if self.channel == "CAN_output":
            self.bus = 0x8f
        self.display_thread = None
        self.shape = None
        self.display = None
        self.canvas = canvas
        self.type = type
        self.x1 = x
        self.y1 = y
        self.x2 = width + x
        self.y2 = height + y
        self.d_x1, self.d_y1, self.d_x2, self.d_y2 = self.x1 + \
            6, self.y1 + 6, self.x2 - 6, self.y2 - 6
        self.create_display()
        if hasattr(self, "bus"):
            self.display_thread = threading.Thread(target=self.update_display)
            self.display_thread.start()

    def create_display(self):
        # Background
        self.shape = self.canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2, fill='grey')

        self.canvas.tag_bind(self.shape, "<Button-1>", self.on_press)

        # Display
        self.display = self.canvas.create_rectangle(
            self.d_x1, self.d_y1, self.d_x2, self.d_y2, fill='black')

    def update_display(self):
        if hasattr(self, "bus"):
            with can.interface.Bus(channel=0, interface="virtual") as bus:
                print("Ready to read")
                for msg in bus:
                    print(msg)
                    return


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
