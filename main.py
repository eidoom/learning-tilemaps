from random import choices, randrange

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
sand_tile = pyglet.resource.image("sand.png")
tree = pyglet.resource.image("tree.png")
stone = pyglet.resource.image("stone.png")
player_image = pyglet.resource.image("player.png")

centre_image(player_image)

tiles = [red_tile, green_tile, blue_tile, black_tile, sand_tile]
weights = [1, 20, 3, 1, 0]
traversability = {red_tile: False, green_tile: True, blue_tile: False, black_tile: False, sand_tile: True}

TILE_SIZE = 40
HALF_TILE_SIZE = TILE_SIZE // 2
MAP_TILE_WIDTH = 32
MAP_TILE_HEIGHT = 18
MAP_TILE_HALF_WIDTH = MAP_TILE_WIDTH // 2
MAP_TILE_HALF_HEIGHT = MAP_TILE_HEIGHT // 2
MAP_PIXEL_WIDTH = MAP_TILE_WIDTH * TILE_SIZE
MAP_PIXEL_HEIGHT = MAP_TILE_HEIGHT * TILE_SIZE
MAP_PIXEL_HALF_WIDTH = MAP_PIXEL_WIDTH // 2
MAP_PIXEL_HALF_HEIGHT = MAP_PIXEL_HEIGHT // 2

tile_map = [[choices(tiles, weights=weights)[0] for _ in range(MAP_TILE_WIDTH)] for _ in range(MAP_TILE_HEIGHT)]
# tile_map = [[red_tile for _ in range(MAP_TILE_WIDTH)] for _ in range(MAP_TILE_HEIGHT)]
tile_map[MAP_TILE_HALF_HEIGHT][MAP_TILE_HALF_WIDTH] = green_tile
tile_map[MAP_TILE_HALF_HEIGHT][MAP_TILE_HALF_WIDTH - 1] = green_tile
tile_map[MAP_TILE_HALF_HEIGHT - 1][MAP_TILE_HALF_WIDTH] = green_tile
tile_map[MAP_TILE_HALF_HEIGHT - 1][MAP_TILE_HALF_WIDTH - 1] = green_tile

for i in range(MAP_TILE_HEIGHT):
    for j in range(MAP_TILE_WIDTH):
        if tile_map[i][j] == blue_tile:
            try:
                for ii in (i - 1, i + 1):
                    if not tile_map[ii][j] == blue_tile:
                        tile_map[ii][j] = sand_tile
                for jj in (j - 1, j + 1):
                    if not tile_map[i][jj] == blue_tile:
                        tile_map[i][jj] = sand_tile
            except IndexError:
                pass

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

game_window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, resizable=True, caption="Tile map game")
game_window.set_maximum_size(MAP_PIXEL_WIDTH, MAP_PIXEL_HEIGHT)
game_window.set_minimum_size(*[TILE_SIZE * 3] * 2)
game_window.set_icon(player_image)

main_batch = pyglet.graphics.Batch()

background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)


def tiles_to_pixels(i_, j_):
    x_ = j_ * TILE_SIZE
    y_ = (MAP_TILE_HEIGHT - 1 - i_) * TILE_SIZE
    return x_, y_


def pixels_to_tiles(x_, y_):
    i_ = -int((y_ // TILE_SIZE) - (MAP_TILE_HEIGHT - 1))
    j_ = int(x_ // TILE_SIZE)
    return i_, j_


class PositionalObject(pyglet.sprite.Sprite):
    def __init__(self, map_x=0, map_y=0, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.map_x = map_x
        self.map_y = map_y

        self.half_width = self.width // 2
        self.half_height = self.height // 2


class MapObject(PositionalObject):
    def __init__(self, traversable=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.traversable = traversable


tile_objects = []
environment_objects = []

for i in range(MAP_TILE_HEIGHT):
    for j in range(MAP_TILE_WIDTH):
        x, y = tiles_to_pixels(i, j)
        tile = tile_map[i][j]
        tile_objects.append(MapObject(
            img=tile, traversable=traversability[tile], map_x=x, map_y=y, batch=main_batch, group=background))
        if tile in (sand_tile, green_tile) and choices([True, False], weights=[1, 10])[0]:
            environment_objects.append(MapObject(
                img=tree, traversable=False, map_x=x + randrange(0, tile.width),
                map_y=y + randrange(0, tile.height), batch=main_batch, group=foreground))
        if tile in (sand_tile, black_tile, green_tile, red_tile) and choices([True, False], weights=[1, 10])[0]:
            environment_objects.append(MapObject(
                img=stone, traversable=True, map_x=x + randrange(0, tile.width),
                map_y=y + randrange(0, tile.height), batch=main_batch, group=foreground))


def nested_ref_to_list_ref(i_, j_):
    return i_ * MAP_TILE_WIDTH + j_


class Player(PositionalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.key_handler = pyglet.window.key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

        self.walking_speed = 100
        self.running_speed = self.walking_speed * 2

    def check_map_bounds(self):
        min_x = self.half_width
        min_y = self.half_height
        max_x = MAP_PIXEL_WIDTH - self.half_width
        max_y = MAP_PIXEL_HEIGHT - self.half_height
        if self.map_x < min_x:
            self.map_x = min_x
        elif self.map_x > max_x:
            self.map_x = max_x
        if self.map_y < min_y:
            self.map_y = min_y
        elif self.map_y > max_y:
            self.map_y = max_y

    def check_traversability(self):

        centre_i, centre_j = pixels_to_tiles(self.map_x, self.map_y)

        tiles_ = []

        for i_ in (centre_i - 1, centre_i, centre_i + 1):
            for j_ in (centre_j - 1, centre_j, centre_j + 1):
                try:
                    tiles_.append(tile_objects[nested_ref_to_list_ref(i_, j_)])
                except IndexError:
                    pass

        for obj in environment_objects + tiles_:
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

        self.check_map_bounds()
        self.check_traversability()


class Camera:
    def __init__(self):
        # Camera position is coordinate of bottom left of visible rectangle.
        self.x = 0
        self.y = 0

    def apply(self, target):
        target.x = target.map_x - self.x
        target.y = target.map_y - self.y

    def update(self, target):
        if target.map_x < game_window.width // 2:
            self.x = 0
            target.x = target.map_x - self.x
        elif target.map_x > MAP_PIXEL_WIDTH - game_window.width // 2:
            self.x = MAP_PIXEL_WIDTH - game_window.width
            target.x = target.map_x - self.x
        else:
            self.x = target.map_x - game_window.width // 2

        if target.map_y < game_window.height // 2:
            self.y = 0
            target.y = target.map_y - self.y
        elif target.map_y > MAP_PIXEL_HEIGHT - game_window.height // 2:
            self.y = MAP_PIXEL_HEIGHT - game_window.height
            target.y = target.map_y - self.y
        else:
            self.y = target.map_y - game_window.height // 2


camera = Camera()

player = Player(img=player_image, x=game_window.width // 2, y=game_window.height // 2, map_x=MAP_PIXEL_HALF_WIDTH,
                map_y=MAP_PIXEL_HALF_HEIGHT, batch=main_batch, group=foreground)

game_objects = [player]

for game_object in game_objects:
    for handler in game_object.event_handlers:
        game_window.push_handlers(handler)


# @game_window.event
# def on_resize(width, height):
#     camera.apply(player)


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


def update(dt):
    camera.update(player)

    for game_object_ in game_objects:
        game_object_.object_update(dt)

    for object_ in tile_objects + environment_objects:
        camera.apply(object_)


UPS = 24


def main():
    pyglet.clock.schedule_interval(update, 1 / UPS)
    pyglet.app.run()


if __name__ == "__main__":
    main()
