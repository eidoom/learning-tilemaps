import pyglet


class GameWindow(pyglet.window.Window):
    def __init__(self, max_width, max_height, min_size, icon, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_maximum_size(max_width, max_height)
        self.set_minimum_size(*[min_size] * 2)
        self.set_icon(icon)


if __name__ == "__main__":
    exit()
