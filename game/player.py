import pyglet

from game import util, character


class Player(character.Character):
    def __init__(self, c_img, l_img, r_img, c_ani, l_ani, r_ani, *args, **kwargs):
        self.walking_speed = 100
        self.running_speed = self.walking_speed * 2
        super().__init__(
            img=c_img, mvmt_spd=self.walking_speed, affinity=None, *args, **kwargs
        )

        self.key_handler = pyglet.window.key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

        controls_raw = {
            "up": "W",
            "left": "A",
            "right": "D",
            "down": "S",
            "run": "LSHIFT",
        }
        self.control = {
            dict_key: getattr(pyglet.window.key, dict_value)
            for dict_key, dict_value in controls_raw.items()
        }

        self.c_img = c_img
        self.l_img = l_img
        self.r_img = r_img
        self.c_ani = c_ani
        self.l_ani = l_ani
        self.r_ani = r_ani

        self.effect = False
        self.effect_x = 0
        self.effect_y = 0

        self.interaction_range = 150

        self.current = None

    def on_key_press(self, symbol, modifiers):
        if symbol is self.control["right"]:
            self.image = self.r_ani
        if symbol is self.control["left"]:
            self.image = self.l_ani
        if symbol in [self.control[key] for key in ("up", "down")]:
            self.image = self.c_ani

    def on_key_release(self, symbol, modifiers):
        def continue_animation(static_image):
            if self.key_handler[self.control["right"]]:
                self.image = self.r_ani
            elif self.key_handler[self.control["left"]]:
                self.image = self.l_ani
            elif any([self.key_handler[self.control[key]] for key in ("up", "down")]):
                self.image = self.c_ani
            else:
                self.image = static_image

        if symbol is self.control["right"]:
            continue_animation(self.r_img)
        if symbol is self.control["left"]:
            continue_animation(self.l_img)
        if symbol in [self.control[key] for key in ("up", "down")]:
            continue_animation(self.c_img)

    def on_mouse_press(self, x, y, button, modifiers):
        if button is pyglet.window.mouse.LEFT:
            if self.current is not None:
                if util.distance((x, y), self.position) < self.interaction_range:
                    self.effect = True
                    self.effect_x = x
                    self.effect_y = y

    def update_obj(self, dt):
        if self.key_handler[self.control["run"]]:
            self.movement_speed = self.running_speed
        else:
            self.movement_speed = self.walking_speed

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
