import pyglet

from game import overlays


class GameWindow(pyglet.window.Window):
    def __init__(self, max_width, max_height, min_size, icon, tile_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tile_size = tile_size

        self.half_width = self.width // 2
        self.half_height = self.height // 2
        self.tile_width = self.width // self.tile_size
        self.tile_height = self.height // self.tile_size

        self.set_maximum_size(max_width, max_height)
        self.set_minimum_size(*[min_size] * 2)
        self.set_icon(icon)

        self.overlay = None

        self.fps_display = pyglet.window.FPSDisplay(self)

    def set_overlay(self, new_overlay):
        if self.overlay:
            self.remove_handlers(self.overlay)
        self.overlay = new_overlay
        if self.overlay:
            self.push_handlers(self.overlay)

    def play(self):
        self.set_overlay(None)

    def open_main_menu(self):
        self.set_overlay(overlays.MainMenu(self))

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            if self.overlay:
                self.play()
            else:
                self.open_main_menu()


if __name__ == "__main__":
    exit()
