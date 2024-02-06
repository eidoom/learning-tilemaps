import pyglet

from sys import exit as sys_exit


class Overlay:
    def update(self, dt):
        pass

    def draw(self):
        pass


class Menu(Overlay):
    def __init__(self, game_window, title):
        self.items = []
        self.font_size = 36
        self.title_text = pyglet.text.Label(
            title,
            x=game_window.width // 2,
            y=game_window.height - self.font_size,
            font_size=self.font_size,
            anchor_x="center",
            anchor_y="center",
        )
        self.selected_index = 0

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.DOWN:
            self.selected_index += 1
        elif symbol == pyglet.window.key.UP:
            self.selected_index -= 1
        self.selected_index = self.selected_index % len(self.items)

    def on_key_release(self, symbol, modifiers):
        self.items[self.selected_index].on_key_release(symbol, modifiers)

    def draw(self):
        self.title_text.draw()
        for i, item in enumerate(self.items):
            item.draw(i == self.selected_index)


class MenuItem:
    def __init__(self, game_window, label, v_pos, activate_func):
        self.v_pos = int(v_pos)
        self.mid_x = game_window.width // 2
        self.mid_y = game_window.height - self.v_pos
        self.font_size = 14
        self.text = pyglet.text.Label(
            label,
            x=self.mid_x,
            y=self.mid_y,
            font_size=self.font_size,
            anchor_x="center",
            anchor_y="center",
        )
        self.width = 100
        self.height = self.font_size * 2
        self.x = self.mid_x - self.width // 2
        self.y = self.mid_y - self.height // 2
        self.default_colour = (
            0,
            0,
            255,
        )
        self.selected_colour = (
            255,
            0,
            0,
        )

        self.activate_func = activate_func

    def draw(self, selected):
        rectangle = pyglet.shapes.Rectangle(
            self.x,
            self.y,
            self.width,
            self.height,
            self.selected_colour if selected else self.default_colour,
        )

        rectangle.draw()

        self.text.draw()

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER and self.activate_func:
            self.activate_func()


class MainMenu(Menu):
    def __init__(self, game_window):
        super().__init__(game_window, "Title")
        self.separation = 50
        self.v_current = 100
        self.items.append(
            MenuItem(game_window, "Play", self.v_current, game_window.play)
        )
        self.v_current += self.separation
        self.items.append(MenuItem(game_window, "Quit", self.v_current, sys_exit))
