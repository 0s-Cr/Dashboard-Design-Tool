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


class IconManager:
    def __init__(self, canvas):
        self.icon_list = []
        self.id_counter = 0
        self.undo_change = []
        self.redo_change = []
        self.canvas = canvas
        self.show_labels = False
        self.label_list = []

    def __str__(self):
        return f"{self.icon_list}"

    def add_icon(self, id, icon):
        self.icon_list.append([id, icon])
        return id

    def add_to_undo(self, id, icon):
        self.undo_change.append([id, icon])


    def toggle_labels(self, event):
        if not self.show_labels:
            for i in self.icon_list:
                print(i[1][1])
                x_centre = (i[1][1][0] + i[1][1][2]) / 2
                print(x_centre)
                y_centre = (i[1][1][1] + i[1][1][3]) / 2
                print(y_centre)
                label = self.canvas.create_text(x_centre, y_centre, text=i[1][0])
                self.label_list.append(label)
                self.show_labels = not self.show_labels
        else:
            for label in self.label_list:
                self.canvas.delete(label)
            self.label_list.clear()
            self.show_labels = not self.show_labels

    def update_icon(self, id, data):
        self.redo_change = []
        for i in range(0, len(self.icon_list)):
            if self.icon_list[i][0] == id:
                self.icon_list[i][1] = data

    def undo_redo(self, event):
        if event == "z" or event.keysym.lower() == "z":
            if self.undo_change != []:
                data = self.undo_change[-1]
                redo_data = [data[0], [data[0], self.canvas.coords(
                    data[0]), self.canvas.itemcget(data[0], "fill")]]
                self.canvas.itemconfig(data[0], fill=data[1][2])
                self.canvas.coords(
                    data[0], data[1][1][0], data[1][1][1], data[1][1][2], data[1][1][3])
                self.redo_change.append(redo_data)
                self.undo_change.pop(-1)
        elif event == "y" or event.keysym.lower() == "y":
            if self.redo_change != []:
                data = self.redo_change[-1]
                undo_data = [data[0], [data[0], self.canvas.coords(
                    data[0]), self.canvas.itemcget(data[0], "fill")]]
                self.canvas.itemconfig(data[0], fill=data[1][2])
                self.canvas.coords(
                    data[0], data[1][1][0], data[1][1][1], data[1][1][2], data[1][1][3])
                self.undo_change.append(undo_data)
                self.redo_change.pop(-1)
