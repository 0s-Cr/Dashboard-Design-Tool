from tkinter import *
import math


class SimIcon:
    def __init__(self, manager, canvas, type, x, y, width, height):
        self.manager = manager
        self.canvas = canvas
        self.type = type
        self.shape = Dial(self.canvas, self.type, 0 ,100, x, y, width, height, 25)


class Dial():
    def __init__(self, canvas, type, min_value, max_value, x, y, width, height, increment):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.type = type
        self.start_angle = 210
        self.radius = min(self.width, self.height) / 2 - 10
        self.center = (x + self.width / 2, y + self.height / 2)
        self.min_value = 0
        self.max_value = max_value
        self.needle = None
        self.increment = increment
        self.create_dial()
        self.update_needle(60)

    def create_dial(self):
        self.canvas.create_oval(
            self.center[0] - self.radius,
            self.center[1] - self.radius,
            self.center[0] + self.radius,
            self.center[1] + self.radius,
            outline="black", width=2,
            fill="light grey"
        )
        step = int(round(240 / (self.max_value / self.increment)))
        number = self.min_value
        for angle in range(self.start_angle, self.start_angle - 241, -step):
            radian = math.radians(angle)
            x = self.center[0] + self.radius * 0.925 * math.cos(radian)
            y = self.center[1] - self.radius * 0.925 * math.sin(radian)
            self.canvas.create_text(x, y, text=str(number), fill="black")
            number += self.increment
        match self.type:
            case "Speed":
                add_text = "MPH"
            case "RPM":
                add_text = "x1000 RPM"
            case "Fuel":
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


if __name__ == "__main__":
    root = Tk()
    root.title("Car Speedometer")
    root.geometry("500x500")

    canvas = Canvas(root, width=500, height=500)
    canvas.pack()

    speedometer = SimIcon(None, canvas, "Fuel", 100, 100, width=300, height=300)

    speed_label = Label(root, text="Speed: 0 mph")
    speed_label.pack()

    # Example usage: Update the speedometer speed

    root.mainloop()
