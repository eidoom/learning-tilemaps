from game import util


class Camera:
    def __init__(self, win_width, win_height, map_width, map_height):
        # Camera position is coordinate of bottom left of visible rectangle.
        self.x = 0
        self.y = 0
        self.win_len_x = win_width
        self.win_len_y = win_height
        self.map_len_x = map_width
        self.map_len_y = map_height
        self.i, self.j = util.pixels_to_tiles(self.x, self.y)
        self.last_i, self.last_j = self.i, self.j

    def initialise(self, target):
        target.map_x = target.x + self.x
        target.map_y = target.y + self.y

    def apply(self, target):
        target.x = target.map_x - self.x
        target.y = target.map_y - self.y

    def set_coord(self, coord, target):
        the_coord = getattr(self, coord)
        map_coord = getattr(target, f"map_{coord}")
        win_lim = getattr(self, f"win_len_{coord}")
        map_lim = getattr(self, f"map_len_{coord}")
        if getattr(target, f"map_{coord}") < win_lim // 2:
            setattr(self, coord, 0)
            setattr(target, coord, map_coord - the_coord)
        elif map_coord > map_lim - win_lim // 2:
            setattr(self, coord, map_lim - win_lim)
            setattr(target, coord, map_coord - the_coord)
        else:
            setattr(self, coord, map_coord - win_lim // 2)

    def update(self, target):
        self.set_coord("x", target)
        self.set_coord("y", target)

        self.last_i, self.last_j = self.i, self.j
        self.i, self.j = util.pixels_to_tiles(self.x, self.y)


if __name__ == "__main__":
    exit()
