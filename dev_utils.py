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

    def clear_area(self):
        for i in self.canvas.getall():
            if i != self.shape:
                i.destroy()

    def check_for_shapes(self):
        overlapping_shapes = []
        x1, y1, x2, y2 = self.canvas.coords(self.shape)
        for i in self.manager.icon_list:
            if i[0] != self.shape:
                other_x1, other_y1, other_x2, other_y2 = i[1][1]
                if (x1 < other_x1 and x2 > other_x2) and (y1 < other_y1 and y2 > other_y2):
                    overlapping_shapes.append(i)
        return overlapping_shapes


class IconManager:
    def __init__(self):
        self.icon_list = []
        self.id_counter = 0

    def __str__(self):
        return f"{self.icon_list}"

    def add_icon(self, id, icon):
        self.icon_list.append([id, icon])
        return id

    def update_icon(self, id, data):
        for i in range(0, len(self.icon_list)):
            if self.icon_list[i][0] == id:
                self.icon_list[i][1] = data
