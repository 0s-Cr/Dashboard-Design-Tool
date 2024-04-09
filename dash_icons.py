import tkinter as tk

class sidebar_icon:
    def __init__(self, canvas, spawn_canvas, type, x, y, width, height, color="blue") -> None:
        self.canvas = canvas
        self.spawn = spawn_canvas
        match type:
            case "Speed":
                self.shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
                self.label_text = "Speedometer"
                self.label = canvas.create_text(x + width / 2, y + height + 10, text=self.label_text)
            case "RPM":
                self.shape = canvas.create_oval(x, y, x + width, y + height, fill=color)
                self.label_text = "Tachometer"
                self.label = canvas.create_text(x + width, y + width * 2 + 10, text=self.label_text)
        self.canvas.tag_bind(self.shape, "<Button-1>", self.spawn_object)

    def spawn_object(self, event):
        x, y = self.canvas.coords(self.shape)[:2]  # Get the top-left corner coordinates of the miniature icon
        icon = movable_icon(self.spawn, x, y, 50, 50)  # Spawn a new instance of MovableIcon at the same position
        

class movable_icon:
    def __init__(self, canvas, x, y, width, height, color="blue"):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x, y, x + width, y + height, fill=color)
        self.canvas.tag_bind(self.rect, "<Button-1>", self.on_press)
        self.canvas.tag_bind(self.rect, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.rect, "<ButtonRelease-1>", self.on_release)
        self.prev_x = 0
        self.prev_y = 0
        self.resizing = False

    def on_press(self, event):
        self.prev_x = event.x
        self.prev_y = event.y
        if event.state & 0x1:
            self.resizing = True
        else:
            self.resizing = False

    def on_drag(self, event):
        if self.resizing:
            width = event.x - self.canvas.coords(self.rect)[0]
            height = event.y - self.canvas.coords(self.rect)[1]
            self.canvas.coords(self.rect, self.canvas.coords(self.rect)[0], self.canvas.coords(self.rect)[1],
                               self.canvas.coords(self.rect)[0] + width, self.canvas.coords(self.rect)[1] + height)
        else:
            new_x = event.x
            new_y = event.y
            self.canvas.move(self.rect, new_x - self.prev_x, new_y - self.prev_y)
            self.prev_x = new_x
            self.prev_y = new_y

    def on_release(self, event):
        self.resizing = False

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Resizable Icon")

    canvas = tk.Canvas(root, width=400, height=300, bg="white")
    canvas.pack()

    # Create a miniature icon at position (10, 10)
    miniature_icon = sidebar_icon(canvas, canvas, "Speed", 10, 10, 30, 30)

    root.mainloop()