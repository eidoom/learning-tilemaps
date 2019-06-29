import pyglet


class PositionalObject(pyglet.sprite.Sprite):
    def __init__(self, map_x=0, map_y=0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.map_x = map_x
        self.map_y = map_y

        self.half_width = self.width // 2
        self.half_height = self.height // 2
        self.radius = (self.half_height + self.half_width) / 2

        self.remove = False


if __name__ == "__main__":
    exit()
