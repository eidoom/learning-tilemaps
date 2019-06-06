import pyglet

import positional_object
import util


class Player(positional_object.PositionalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.key_handler = pyglet.window.key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

        self.walking_speed = 100
        self.running_speed = self.walking_speed * 2

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

    def check_traversability(self, tile_objs, env_objs):

        centre_i, centre_j = util.pixels_to_tiles(self.map_x, self.map_y)

        tiles = []

        for i_ in (centre_i - 1, centre_i, centre_i + 1):
            for j_ in (centre_j - 1, centre_j, centre_j + 1):
                try:
                    tiles.append(tile_objs[util.nested_ref_to_list_ref(i_, j_)])
                except IndexError:
                    pass

        for obj in env_objs + tiles:
            left = obj.map_x - self.half_width
            right = obj.map_x + obj.width + self.half_width
            bottom = obj.map_y - self.half_height
            top = obj.map_y + obj.height + self.half_height

            if all([left < self.map_x < right, bottom < self.map_y < top, not obj.traversable]):

                border = 10
                if bottom + border < self.map_y < top - border:
                    if self.map_x < obj.map_x + obj.half_width:
                        self.map_x = left
                    elif self.map_x > obj.map_x + obj.half_width:
                        self.map_x = right

                elif left + border < self.map_x < right - border:
                    if self.map_y < obj.map_y + obj.half_height:
                        self.map_y = bottom
                    elif self.map_y > obj.map_y + obj.half_height:
                        self.map_y = top

    def object_update(self, dt):
        controls_raw = {
            "up": "W",
            "left": "A",
            "right": "D",
            "down": "S",
            "run": "LSHIFT"
        }
        control = {dict_key: getattr(pyglet.window.key, dict_value) for dict_key, dict_value in controls_raw.items()}

        if self.key_handler[control["run"]]:
            movement_speed = self.running_speed
        else:
            movement_speed = self.walking_speed

        if self.key_handler[control["left"]]:
            self.map_x -= movement_speed * dt
        if self.key_handler[control["right"]]:
            self.map_x += movement_speed * dt
        if self.key_handler[control["up"]]:
            self.map_y += movement_speed * dt
        if self.key_handler[control["down"]]:
            self.map_y -= movement_speed * dt
