from random import choices

import pyglet

pyglet.resource.path = ['resources']
pyglet.resource.reindex()

red_tile = pyglet.resource.image("red.png")
green_tile = pyglet.resource.image("green.png")
blue_tile = pyglet.resource.image("blue.png")
black_tile = pyglet.resource.image("black.png")

tiles = [red_tile, green_tile, blue_tile, black_tile]
weights = [10, 10, 20, 10]

TILE_SIZE = 40
MAP_WIDTH = 16
MAP_HEIGHT = 10

tilemap = [[choices(tiles, weights=weights)[0] for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

game_window = pyglet.window.Window(width=MAP_WIDTH * TILE_SIZE, height=MAP_HEIGHT * TILE_SIZE)

main_batch = pyglet.graphics.Batch()

background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)


def tile_to_coord(i_, j_):
    x = j_ * TILE_SIZE
    y = (MAP_HEIGHT - 1 - i_) * TILE_SIZE
    return x, y


sprites = []

for i in range(MAP_HEIGHT):
    for j in range(MAP_WIDTH):
        x, y = tile_to_coord(i, j)
        sprites.append(pyglet.sprite.Sprite(img=tilemap[i][j], x=x, y=y, batch=main_batch, group=background))


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


def main():
    pyglet.app.run()


if __name__ == "__main__":
    main()
