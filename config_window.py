import tkinter as tk
from tkinter import colorchooser

class ConfigWindow(tk.Toplevel):
    def __init__(self, parent, movable_icon):
        super().__init__(parent)
        self.window = tk.Toplevel
        self.movable_icon = movable_icon
        self.title("Icon Configuration")
        self.geometry("300x150")

        self.color = self.movable_icon.canvas.itemcget(self.movable_icon.shape, "fill")
        color_label = tk.Label(self, text="Colour:")
        color_label.pack()

        self.color_indicator = tk.Canvas(self, width=20, height=20, bg=self.color)
        self.color_indicator.pack()

        self.color_button = tk.Button(self, text="Choose Colour", command=self.choose_color)
        self.color_button.pack()

        preview_frame = tk.Frame(self)
        preview_frame.pack()
        self.preview_shape = self.movable_icon

        apply_cancel_frame = tk.Frame(self)
        apply_cancel_frame.pack(side=tk.BOTTOM)

        cancel_button = tk.Button(apply_cancel_frame, text="Close", command=self.destroy)
        cancel_button.pack(side=tk.LEFT)

        apply_button = tk.Button(apply_cancel_frame, text="Apply", command=self.apply_changes)
        apply_button.pack(side=tk.RIGHT)

        self.grab_set()


    def choose_color(self):
        self.color = colorchooser.askcolor(title="Choose Colour")
        self.color_indicator.config(bg=self.color[1])

    def apply_changes(self):
        if hasattr(self, 'color'):
            self.movable_icon.change_colour(self.color[1])
