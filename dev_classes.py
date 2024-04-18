class DevArea:
    def __init__(self, canvas, x, y, width, height, color="white"):#
        self.canvas = canvas
        self.shape = canvas.create_rectangle(x, y, x+ width, y + height, fill= color)
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
        for shape_id in self.canvas.find_all():
            if shape_id != self.shape:
                other_x1, other_y1, other_x2, other_y2 = self.canvas.coords(shape_id)
                if (x1 < other_x2 and x2 > other_x1) and (y1 < other_y2 and y2 > other_y1):
                    shape_tags = self.canvas.gettags(shape_id)
                    if shape_tags:  # Check if tags exist
                        shape_type = shape_tags[0]
                        overlapping_shapes.append((shape_id, shape_type))
        print(self.canvas.find_all())
        return overlapping_shapes
    