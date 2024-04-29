import math
import threading
from tkinter import *
from tkinter import font

import can

from config_window import *


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
                self.shape = Dial(self.manager, self.canvas, self.type, min_value,
                                  max_value, x, y, width, height, increment, channel)
            case "Logger":
                self.shape = DigitalDisplay(
                    self.canvas, self.type, x, y, width, height, channel)
        manager.add_icon(self)

    def kill_all(self):
        if hasattr(self.shape, "display_thread"):
            self.shape.kill_thread = True
            if self.shape.display_thread != None:
                self.shape.display_thread.join(5.0)


class Dial():
    def __init__(self, manager, canvas, type, min_value, max_value, x, y, width, height, increment, channel):
        self.manager = manager
        self.canvas = canvas
        self.shape = None
        match channel:
            case "Speed":
                self.channel = 0
            case "RPM":
                self.channel = 1
            case "Fuel":
                self.channel = 2
            case "Voltage":
                self.channel = 3
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
            round(240 / ((self.max_value - self.min_value) / self.increment)))
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

    def update_needle(self, target_percentage):
        if self.needle:
            self.canvas.delete(self.needle)
        if target_percentage == 0:
            angle = self.start_angle
        else:
            angle = self.start_angle - (target_percentage / 100) * 240
        radian = math.radians(angle)
        x = self.center[0] + self.radius * 0.85 * math.cos(radian)
        y = self.center[1] - self.radius * 0.85 * math.sin(radian)
        self.needle = self.canvas.create_line(
            self.center[0], self.center[1], x, y, fill="red", width=2
        )
        if self.channel == 3:
            self.manager.voltage_fault.set("Off")
            self.manager.voltage_warning.set("Off")
            self.manager.power_fault.set("Off")
            self.manager.power_warning.set("Off")
            if target_percentage <= 20:
                self.manager.power_warning.set("On")
                if target_percentage <= 3:
                    self.manager.power_fault.set("On")
            elif target_percentage > 75:
                self.manager.voltage_warning.set("On")
                if target_percentage > 85:
                    self.manager.voltage_fault.set("On")
            self.manager.on_combobox_selected(event=None)

    def update_labels(self, min_value, max_value, increment):
        self.min_value, self.max_value, self.increment = min_value, max_value, increment
        if self.labels != []:
            for label in self.labels:
                self.canvas.delete(label)
            self.labels.clear()
        step = int(
            round(240 / ((self.max_value - self.min_value) / self.increment)))
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
        self.data_text = None
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
            self.kill_thread = False
            self.display_thread = threading.Thread(target=self.update_display)
            self.display_thread.start()

    def create_display(self):
        # Background
        self.shape = self.canvas.create_rectangle(
            self.x1, self.y1, self.x2, self.y2, fill='grey')

        # Display
        self.data_text = Text(self.canvas, background="black")
        self.data_text.place(x=self.d_x1, y=self.d_y1, width=int(
            self.d_x2 - self.d_x1), height=int(self.d_y2 - self.d_y1))

    def update_display(self):
        if hasattr(self, "bus"):
            while not self.kill_thread:
                with can.interface.Bus(channel=0, interface="virtual") as bus:
                    for msg in bus:
                        self.data_text.delete(1.0, END)
                        if self.kill_thread:
                            break
                        font_size = font.Font(font=self.data_text["font"])
                        max_display = int(
                            (self.d_y2 - self.d_y1) / (font_size.actual()["size"]) / (4 / 3)) - 1
                        for i in range(0, min(max_display, len(list(msg.data)))):
                            data = list(msg.data)
                            if data[i] < 16 or data[i] == 0xFF:
                                self.data_text.insert(
                                    END, hex(data[i]) + " " + self.match_hex(data[i]), "red")
                                self.data_text.insert(END, '\n')
                            else:
                                self.data_text.insert(
                                    END, hex(data[i]) + " " + self.match_hex(data[i]), "orange")
                                self.data_text.insert(END, '\n')
                            self.data_text.tag_configure(
                                "red", foreground="red")
                            self.data_text.tag_configure(
                                "orange", foreground="orange")
                        print(msg)
                    bus.shutdown()

    def match_hex(self, code):
        match code:
            case 0x00:
                return "BADPARAS"
            case 0x01:
                return "POWER FAULT"
            case 0x02:
                return "RFE FAULT"
            case 0x03:
                return "BUS TIMEOUT"
            case 0x04:
                return "FEEDBACK"
            case 0x05 | 0x15:
                return "POWERVOLTAGE"
            case 0x06 | 0x16:
                return "MOTORTEMP"
            case 0x07 | 0x17:
                return "DEVICETEMP"
            case 0x08 | 0x18:
                return "OVERVOLTAGE"
            case 0x09 | 0x18:
                return "I_PEAK"
            case 0x0A | 0x19:
                return "RACEAWAY"
            case 0x0B:
                return "USER"
            case 0x0E:
                return "CPU-ERROR"
            case 0x0F:
                return "BALLAST"
            case 0x1C:
                return "I2R"
            case _:
                return "UNSPECIFIED ERROR"


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
