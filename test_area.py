import tkinter as tk
import math

class Speedometer():
    def __init__(self, master, start_angle, max_speed, increment = 10, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.width = kwargs.get("width", 200)
        self.height = kwargs.get("height", 200)
        self.start_angle = 210
        self.radius = min(self.width, self.height) / 2 - 10
        self.center = (self.width / 2, self.height / 2)
        self.max_speed = max_speed
        self.needle = None
        self.increment = increment
        self.create_speedometer()

    def create_speedometer(self):
        self.create_oval(
            self.center[0] - self.radius,
            self.center[1] - self.radius,
            self.center[0] + self.radius,
            self.center[1] + self.radius,
            outline="black", width=2,
            fill = "light grey"
        )
        step = int(round(240 / (self.max_speed / 10)))
        number = 0
        for angle in range(self.start_angle, self.start_angle - 241, -step):
            radian = math.radians(angle)
            angle_from_start = -1*(angle - 210)
            x = self.center[0] + self.radius * 0.925 * math.cos(radian)
            y = self.center[1] - self.radius * 0.925 * math.sin(radian)
            self.create_text(x, y, text=str(number), fill="black")
            number += self.increment

    def update_speed(self, speed):
        if self.needle:
            self.delete(self.needle)
        if speed == 0:
            angle = self.start_angle
        else:
            target_pos = speed / self.max_speed
            angle = self.start_angle - target_pos * 240
        radian = math.radians(angle)
        x = self.center[0] + self.radius * 0.85 * math.cos(radian)
        y = self.center[1] - self.radius * 0.85 *  math.sin(radian)
        self.needle = self.create_line(
            self.center[0], self.center[1], x, y, fill="red", width=2
        )

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Car Speedometer")
    
    canvas = tk.Canvas(root, width = 300, height = 300)

    speedometer = Speedometer(root, width=300, height=300)
    speedometer.pack()

    speed_label = tk.Label(root, text="Speed: 0 mph")
    speed_label.pack()

    def update_speedometer(speed):
        speedometer.update_speed(speed)
        speed_label.config(text=f"Speed: {speed} mph")

    # Example usage: Update the speedometer speed
    update_speedometer(60)

    root.mainloop()
