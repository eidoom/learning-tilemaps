import pyglet

from game import util, character


class Player(character.Character):
    def __init__(self, c_img, l_img, r_img, c_ani, l_ani, r_ani, *args, **kwargs):
        self.walking_speed = 100
        self.running_speed = self.walking_speed * 2
        super().__init__(img=c_img, mvmt_spd=self.walking_speed, *args, **kwargs)

        self.key_handler = pyglet.window.key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

        controls_raw = {
            "up": "W",
            "left": "A",
            "right": "D",
            "down": "S",
            "run": "LSHIFT"
        }
        self.control = {
            dict_key: getattr(pyglet.window.key, dict_value) for dict_key, dict_value in controls_raw.items()}

        self.c_img = c_img
        self.l_img = l_img
        self.r_img = r_img
        self.c_ani = c_ani
        self.l_ani = l_ani
        self.r_ani = r_ani

    def check_traversability(self, tile_objs, env_obj_dict, max_width, max_height):

        centre_i, centre_j = util.pixels_to_tiles(self.map_x, self.map_y)

        tiles = []

        def add_tile(i_, j_):
            try:
                tiles.append(tile_objs[util.nested_ref_to_list_ref(i_, j_)])
            except IndexError:
                pass

        for i in [centre_i + ii for ii in (-1, 1)]:
            for j in [centre_j + jj for jj in range(-1, 2)]:
                add_tile(i, j)

        for j in [centre_j + jj for jj in (-1, 1)]:
            add_tile(centre_i, j)

        env_objs = []

        for x in [int(self.map_x) + xx for xx in range(-int(self.half_width + max_width + 1), self.half_width + 1)]:
            for y in [int(self.map_y) + yy for yy in
                      range(-int(self.half_height + max_height + 1), self.half_height + 1)]:
                try:
                    env_objs.append(env_obj_dict[(x, y)])
                except KeyError:
                    pass

        for obj in tiles + env_objs:
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

    def on_key_press(self, symbol, modifiers):
        if symbol is self.control["run"]:
            self.movement_speed = self.running_speed
        if symbol is self.control["right"]:
            self.image = self.r_ani
        if symbol is self.control["left"]:
            self.image = self.l_ani
        if symbol in [self.control[key] for key in ("up", "down")]:
            self.image = self.c_ani

    def on_key_release(self, symbol, modifiers):
        if symbol is self.control["run"]:
            self.movement_speed = self.walking_speed
        if not any([self.key_handler[self.control[key]] for key in ("left", "right", "up", "down")]):
            if symbol is self.control["right"]:
                self.image = self.r_img
            if symbol is self.control["left"]:
                self.image = self.l_img
            if symbol in [self.control[key] for key in ("up", "down")]:
                self.image = self.c_img

    def update_obj(self, dt):

        if self.key_handler[self.control["left"]]:
            self.map_x -= self.movement_speed * dt
        if self.key_handler[self.control["right"]]:
            self.map_x += self.movement_speed * dt
        if self.key_handler[self.control["up"]]:
            self.map_y += self.movement_speed * dt
        if self.key_handler[self.control["down"]]:
            self.map_y -= self.movement_speed * dt


if __name__ == "__main__":
    exit()
