class DevArea:
    def __init__(self, manager, canvas, x, y, width, height, color="white"):
        self.manager = manager
        self.canvas = canvas
        self.shape = canvas.create_rectangle(
            x, y, x + width, y + height, fill=color)
        self.canvas.tag_bind(self.shape, "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind(self.shape, "<Button-1>", self.on_press)

    def on_drag(self, event):
        width = event.x - self.canvas.coords(self.shape)[0]
        height = event.y - self.canvas.coords(self.shape)[1]
        self.canvas.coords(self.shape, self.canvas.coords(self.shape)[0], self.canvas.coords(self.shape)[1],
                           self.canvas.coords(self.shape)[0] + width, self.canvas.coords(self.shape)[1] + height)

    def on_press(self, event):
        if event.state & 0x4:
            print(self.check_for_shapes())

    def check_for_shapes(self):
        overlapping_shapes = []
        x1, y1, x2, y2 = self.canvas.coords(self.shape)
        for i in self.manager.icon_list:
            if i[0] != self.shape:
                other_x1, other_y1, other_x2, other_y2 = i[1][1]
                if (x1 < other_x1 and x2 > other_x2) and (y1 < other_y1 and y2 > other_y2):
                    overlapping_shapes.append(i)
        return overlapping_shapes

    def get_coords(self):
        return self.canvas.coords(self.shape)
