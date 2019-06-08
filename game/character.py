from game import positional_object


class Character(positional_object.PositionalObject):
    def __init__(self, mvmt_spd, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.movement_speed = mvmt_spd

    def check_map_bounds(self, map_width, map_height):
        min_x = self.half_width
        min_y = self.half_height
        max_x = map_width - self.half_width
        max_y = map_height - self.half_height
        if self.map_x < min_x:
            self.map_x = min_x
        elif self.map_x > max_x:
            self.map_x = max_x
        if self.map_y < min_y:
            self.map_y = min_y
        elif self.map_y > max_y:
            self.map_y = max_y


if __name__ == "__main__":
    exit()
