class Wall:
    def __init__(self, pos_x, pos_y, width, height):
        self.name = 'wall'
        self.x = pos_x
        self.y = pos_y
        self.width = width
        self.height = height
        self.top = pos_y
        self.bottom = pos_y + self.height
        self.right = pos_x + self.width
        self.left = pos_x

    def __str__(self):
        return self.name