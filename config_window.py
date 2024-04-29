import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk


class DevConfigWindow(tk.Toplevel):
    def __init__(self, parent, canvas, movable_icon):
        super().__init__(parent)
        self.window = tk.Toplevel
        self.movable_icon = movable_icon
        self.type = self.movable_icon.type
        self.title(f"{self.type} Configuration")
        self.geometry("300x200")

        # Entry for color selection
        self.color = self.movable_icon.canvas.itemcget(
            self.movable_icon.shape, "fill")
        color_label = tk.Label(self, text="Color:")
        color_label.pack()

        self.color_indicator = tk.Canvas(
            self, width=20, height=20, bg=self.color)
        self.color_indicator.pack()

        self.color_button = tk.Button(
            self, text="Choose Color", command=self.choose_color)
        self.color_button.pack()

        # Entry for X and Y coordinates
        position_frame = tk.Frame(self)
        position_frame.pack()

        x1, y1, x2, y2 = canvas.coords(self.movable_icon.shape)

        tk.Label(position_frame, text="X Coordinate:").grid(row=0, column=0)
        self.x_entry = tk.Entry(position_frame)
        self.x_entry.insert(0, str(x1))
        self.x_entry.grid(row=0, column=1)

        tk.Label(position_frame, text="Y Coordinate:").grid(row=1, column=0)
        self.y_entry = tk.Entry(position_frame)
        self.y_entry.insert(0, str(y1))
        self.y_entry.grid(row=1, column=1)

        tk.Label(position_frame, text="Width:").grid(row=2, column=0)
        self.w_entry = tk.Entry(position_frame)
        self.w_entry.insert(
            0, str(abs(x1 - x2)))
        self.w_entry.grid(row=2, column=1)

        if self.movable_icon.type not in ["Speed", "RPM", "Fuel Temp", "Volt Circle"]:
            tk.Label(position_frame, text="Height:").grid(row=3, column=0)
            self.h_entry = tk.Entry(position_frame)
            self.h_entry.insert(
                0, str(abs(y1 - y2)))
            self.h_entry.grid(row=3, column=1)

        # Apply and cancel buttons
        apply_cancel_frame = tk.Frame(self)
        apply_cancel_frame.pack(side=tk.BOTTOM)

        cancel_button = tk.Button(
            apply_cancel_frame, text="Close", command=self.destroy)
        cancel_button.pack(side=tk.LEFT)

        apply_button = tk.Button(
            apply_cancel_frame, text="Apply", command=self.apply_changes)
        apply_button.pack(side=tk.RIGHT)
        self.grab_set()

    def choose_color(self):
        self.color = colorchooser.askcolor(title="Choose Color")
        self.color_indicator.config(bg=self.color[1])

    def apply_changes(self):
        if hasattr(self, 'color') and len(self.color[1]) >= 3:
            self.movable_icon.change_color(self.color[1])
        x, y, w, = float(self.x_entry.get()), float(self.y_entry.get()), float(
            self.w_entry.get())
        if self.movable_icon.type in ["Speed", "RPM", "Fuel Temp", "Volt Circle"]:
            h = w
        else:
            h = float(self.h_entry.get())
        self.movable_icon.change_pos(x, y, w, h)


class SimConfigWindow(tk.Toplevel):
    def __init__(self, parent, canvas, sim_icon):
        super().__init__(parent)
        self.window = tk.Toplevel
        self.sim_icon = sim_icon
        self.type = self.sim_icon.type
        self.title(f"{self.type} Configuration")
        self.geometry("300x200")

        # Entry for config options
        sim_entry_frame = tk.Frame(self)
        sim_entry_frame.pack()

        tk.Label(sim_entry_frame, text="Maximum Value:").grid(row=0, column=0)
        self.max_entry = tk.Entry(sim_entry_frame)
        self.max_entry.insert(0, str(sim_icon.max_value))
        self.max_entry.grid(row=0, column=1)

        tk.Label(sim_entry_frame, text="Minimum Value:").grid(row=1, column=0)
        self.min_entry = tk.Entry(sim_entry_frame)
        self.min_entry.insert(0, str(sim_icon.min_value))
        self.min_entry.grid(row=1, column=1)

        tk.Label(sim_entry_frame, text="Increment:").grid(row=2, column=0)
        self.inc_entry = tk.Entry(sim_entry_frame)
        self.inc_entry.insert(0, str(sim_icon.increment))
        self.inc_entry.grid(row=2, column=1)

        packed_selections = tk.Frame(self)
        packed_selections.pack()

        match self.type:
            case "Speed":
                self.unit_select = ttk.Combobox(
                    packed_selections, values=["MPH", "Km/h"])
                self.unit_select.set(self.sim_icon.add_text)
                self.unit_select.pack()

        # Apply and cancel buttons
        apply_cancel_frame = tk.Frame(self)
        apply_cancel_frame.pack(side=tk.BOTTOM)

        cancel_button = tk.Button(
            apply_cancel_frame, text="Close", command=self.destroy)
        cancel_button.pack(side=tk.LEFT)

        apply_button = tk.Button(
            apply_cancel_frame, text="Apply", command=self.apply_changes)
        apply_button.pack(side=tk.RIGHT)
        self.grab_set()

    def apply_changes(self):
        if hasattr(self, "unit_select"):
            self.sim_icon.add_text = self.unit_select.get()
        self.sim_icon.update_labels(int(self.min_entry.get()), int(
            self.max_entry.get()), int(self.inc_entry.get()))
