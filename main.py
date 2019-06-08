from random import choices, randrange

import pyglet

from game import camera, util, player, map_object, resources as r, npc
import parameters as p

weights = [1, 20, 3, 1, 0]
traversability = {r.red_tile: False, r.green_tile: True, r.blue_tile: False, r.black_tile: False, r.sand_tile: True}

tile_map = [[choices(r.tile_imgs, weights=weights)[0] for _ in range(p.MAP_TILE_WIDTH)] for _ in
            range(p.MAP_TILE_HEIGHT)]
tile_map[p.MAP_TILE_HALF_HEIGHT][p.MAP_TILE_HALF_WIDTH] = r.green_tile
tile_map[p.MAP_TILE_HALF_HEIGHT][p.MAP_TILE_HALF_WIDTH + 1] = r.green_tile
tile_map[p.MAP_TILE_HALF_HEIGHT - 1][p.MAP_TILE_HALF_WIDTH] = r.green_tile
tile_map[p.MAP_TILE_HALF_HEIGHT - 1][p.MAP_TILE_HALF_WIDTH + 1] = r.green_tile

for i in range(p.MAP_TILE_HEIGHT):
    for j in range(p.MAP_TILE_WIDTH):
        if tile_map[i][j] == r.blue_tile:
            try:
                for ii in (i - 1, i + 1):
                    if not tile_map[ii][j] == r.blue_tile:
                        tile_map[ii][j] = r.sand_tile
                for jj in (j - 1, j + 1):
                    if not tile_map[i][jj] == r.blue_tile:
                        tile_map[i][jj] = r.sand_tile
            except IndexError:
                pass

game_window = pyglet.window.Window(width=p.WINDOW_WIDTH, height=p.WINDOW_HEIGHT, resizable=True, caption=p.GAME_NAME)
game_window.set_maximum_size(p.MAP_PIXEL_WIDTH, p.MAP_PIXEL_HEIGHT)
game_window.set_minimum_size(*[p.TILE_SIZE * 3] * 2)
game_window.set_icon(r.player_image)

main_batch = pyglet.graphics.Batch()

background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

tile_objs = []
env_obj_dict = {}

max_height = max([img.height for img in r.env_imgs])
max_width = max([img.width for img in r.env_imgs])

for i in range(p.MAP_TILE_HEIGHT):
    for j in range(p.MAP_TILE_WIDTH):
        x, y = util.tiles_to_pixels(i, j)
        tile = tile_map[i][j]
        tile_objs.append(map_object.MapObject(
            img=tile, traversable=traversability[tile], map_x=x, map_y=y, batch=main_batch, group=background))
        if choices([True, False], weights=[1, 9])[0]:
            obj_x = x + randrange(0, tile.width)
            obj_y = y + randrange(0, tile.height)
            if tile in (r.green_tile,):
                obj = map_object.MapObject(img=r.tree, traversable=False, map_x=obj_x, map_y=obj_y, batch=main_batch,
                                           group=foreground)
            elif tile in (r.black_tile, r.sand_tile):
                obj = map_object.MapObject(img=r.stone, traversable=True, map_x=obj_x, map_y=obj_y, batch=main_batch,
                                           group=foreground)
            try:
                env_obj_dict.update({(obj_x, obj_y): obj})
            except NameError:
                pass

scale = p.TILE_SIZE / r.tile_imgs[0].width

for tile in tile_objs:
    tile.scale = scale

cam = camera.Camera(game_window.width, game_window.height, p.MAP_PIXEL_WIDTH, p.MAP_PIXEL_HEIGHT)


def generate_position():
    return randrange(0, p.MAP_PIXEL_WIDTH), randrange(0, p.MAP_PIXEL_HEIGHT)


ai_characters = []

for _ in range(5 * p.MAP_TILE_SCALE):
    pos = generate_position()
    ai_characters.append(npc.NPC(img=r.char_npc_air, map_x=pos[0], map_y=pos[1], group=foreground, batch=main_batch))

protagonist = player.Player(
    c_img=r.player_image, l_img=r.player_left_image, r_img=r.player_right_image,
    c_ani=r.player_animation, l_ani=r.player_left_animation, r_ani=r.player_right_animation,
    x=game_window.width // 2, y=game_window.height // 2, map_x=p.MAP_PIXEL_HALF_WIDTH, map_y=p.MAP_PIXEL_HALF_HEIGHT,
    batch=main_batch, group=foreground)

input_objs = [protagonist]

for input_obj in input_objs:
    for handler in input_obj.event_handlers:
        game_window.push_handlers(handler)

dynamic_objs = input_objs + ai_characters


# @game_window.event
# def on_resize(width, height):
#     cam.apply(protagonist)


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


def update(dt):
    cam.update(protagonist)

    for dy_obj in dynamic_objs:
        dy_obj.update_obj(dt)
        dy_obj.check_map_bounds(p.MAP_PIXEL_WIDTH, p.MAP_PIXEL_HEIGHT)

    protagonist.check_traversability(tile_objs, env_obj_dict, max_width, max_height)

    for object_ in tile_objs + list(env_obj_dict.values()) + ai_characters:
        cam.apply(object_)

    # fps = pyglet.clock.get_fps()
    # print(fps)


def main():
    pyglet.clock.schedule_interval(update, 1 / p.UPS)
    pyglet.app.run()


if __name__ == "__main__":
    main()
