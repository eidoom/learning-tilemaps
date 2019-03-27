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
weights = [10, 10, 20, 10]

TILE_SIZE = 40
MAP_TILE_WIDTH = 16
MAP_TILE_HEIGHT = 10
MAP_COORD_WIDTH = MAP_TILE_WIDTH * TILE_SIZE
MAP_COORD_HEIGHT = MAP_TILE_HEIGHT * TILE_SIZE

tilemap = [[choices(tiles, weights=weights)[0] for _ in range(MAP_TILE_WIDTH)] for _ in range(MAP_TILE_HEIGHT)]

game_window = pyglet.window.Window(width=MAP_TILE_WIDTH * TILE_SIZE, height=MAP_TILE_HEIGHT * TILE_SIZE)

main_batch = pyglet.graphics.Batch()

background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)


def tile_to_coord(i_, j_):
    x = j_ * TILE_SIZE
    y = (MAP_TILE_HEIGHT - 1 - i_) * TILE_SIZE
    return x, y


sprites = []

for i in range(MAP_TILE_HEIGHT):
    for j in range(MAP_TILE_WIDTH):
        x, y = tile_to_coord(i, j)
        sprites.append(pyglet.sprite.Sprite(img=tilemap[i][j], x=x, y=y, batch=main_batch, group=background))


class Player(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.key_handler = pyglet.window.key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

        self.movement_speed = 100

    def object_update(self, dt):
        controls_raw = {
            "up": "W",
            "left": "A",
            "right": "D",
            "down": "S",
        }
        control = {dict_key: getattr(pyglet.window.key, dict_value) for dict_key, dict_value in controls_raw.items()}

        if self.key_handler[control["left"]]:
            self.x -= self.movement_speed * dt
        if self.key_handler[control["right"]]:
            self.x += self.movement_speed * dt
        if self.key_handler[control["up"]]:
            self.y += self.movement_speed * dt
        if self.key_handler[control["down"]]:
            self.y -= self.movement_speed * dt


player = Player(img=player_image, x=MAP_COORD_WIDTH // 2, y=MAP_COORD_HEIGHT // 2, batch=main_batch, group=foreground)

game_objects = [player]

for game_object in game_objects:
    for handler in game_object.event_handlers:
        game_window.push_handlers(handler)


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


def update(dt):
    for game_object_ in game_objects:
        game_object_.object_update(dt)


def main():
    pyglet.clock.schedule_interval(update, 1 / 60.0)

    pyglet.app.run()


if __name__ == "__main__":
    main()
