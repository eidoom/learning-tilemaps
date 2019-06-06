class Camera:
    def __init__(self, win_width, win_height, map_width, map_height):
        # Camera position is coordinate of bottom left of visible rectangle.
        self.x = 0
        self.y = 0
        self.win_width = win_width
        self.win_height = win_height
        self.map_width = map_width
        self.map_height = map_height

    def apply(self, target):
        target.x = target.map_x - self.x
        target.y = target.map_y - self.y

    def update(self, target):
        if target.map_x < self.win_width // 2:
            self.x = 0
            target.x = target.map_x - self.x
        elif target.map_x > self.map_width - self.win_width // 2:
            self.x = self.map_width - self.win_width
            target.x = target.map_x - self.x
        else:
            self.x = target.map_x - self.win_width // 2

        if target.map_y < self.win_height // 2:
            self.y = 0
            target.y = target.map_y - self.y
        elif target.map_y > self.map_height - self.win_height // 2:
            self.y = self.map_height - self.win_height
            target.y = target.map_y - self.y
        else:
            self.y = target.map_y - self.win_height // 2
