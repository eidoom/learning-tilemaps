from random import choices

import pyglet

pyglet.resource.path = ['resources']
pyglet.resource.reindex()


def centre_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


red_tile = pyglet.resource.image("red.png")
green_tile = pyglet.resource.image("green.png")
blue_tile = pyglet.resource.image("blue.png")
black_tile = pyglet.resource.image("black.png")
player_image = pyglet.resource.image("player.png")

centre_image(player_image)

tiles = [red_tile, green_tile, blue_tile, black_tile]
weights = [5, 20, 30, 5]

TILE_SIZE = 40
MAP_TILE_WIDTH = 16 * 2
MAP_TILE_HEIGHT = 10 * 2
MAP_PIXEL_WIDTH = MAP_TILE_WIDTH * TILE_SIZE
MAP_PIXEL_HEIGHT = MAP_TILE_HEIGHT * TILE_SIZE

tile_map = [[choices(tiles, weights=weights)[0] for _ in range(MAP_TILE_WIDTH)] for _ in range(MAP_TILE_HEIGHT)]

WINDOW_WIDTH = 500
WINDOW_HALF_WIDTH = WINDOW_WIDTH // 2
WINDOW_HEIGHT = 500
WINDOW_HALF_HEIGHT = WINDOW_HEIGHT // 2

game_window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

main_batch = pyglet.graphics.Batch()

background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)


def tiles_to_pixels(i_, j_):
    x_ = j_ * TILE_SIZE
    y_ = (MAP_TILE_HEIGHT - 1 - i_) * TILE_SIZE
    return x_, y_


sprites = []

for i in range(MAP_TILE_HEIGHT):
    for j in range(MAP_TILE_WIDTH):
        x, y = tiles_to_pixels(i, j)
        sprites.append(pyglet.sprite.Sprite(img=tile_map[i][j], x=x, y=y, batch=main_batch, group=background))


class Player(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.key_handler = pyglet.window.key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

        self.walking_speed = 100
        self.running_speed = self.walking_speed * 2

    def check_bounds(self):
        min_x = self.width // 2
        min_y = self.height // 2
        max_x = MAP_PIXEL_WIDTH - self.width // 2
        max_y = MAP_PIXEL_HEIGHT - self.height // 2
        if self.x < min_x:
            self.x = min_x
        elif self.x > max_x:
            self.x = max_x
        if self.y < min_y:
            self.y = min_y
        elif self.y > max_y:
            self.y = max_y

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
            self.x -= movement_speed * dt
        if self.key_handler[control["right"]]:
            self.x += movement_speed * dt
        if self.key_handler[control["up"]]:
            self.y += movement_speed * dt
        if self.key_handler[control["down"]]:
            self.y -= movement_speed * dt

        self.check_bounds()


# class Camera:
#     def __init__(self):
#         self.x = 0
#         self.y = 0
#
#     def apply(self, target, dt):
#         target.x += self.x * dt
#         target.y += self.y * dt
#
#     def update(self, target):
#         self.x = WINDOW_HALF_WIDTH - target.x
#         self.y = WINDOW_HALF_HEIGHT - target.y
#
#
# camera = Camera()

player = Player(img=player_image, x=WINDOW_HALF_WIDTH, y=WINDOW_HALF_HEIGHT, batch=main_batch, group=foreground)

game_objects = [player]

for game_object in game_objects:
    for handler in game_object.event_handlers:
        game_window.push_handlers(handler)


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


def update(dt):
    # camera.update(player)

    for game_object_ in game_objects:
        game_object_.object_update(dt)

    # for sprite in sprites:
    #     camera.apply(sprite, dt)


def main():
    pyglet.clock.schedule_interval(update, 1 / 60.0)
    pyglet.app.run()


if __name__ == "__main__":
    main()
