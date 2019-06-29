#!/usr/bin/env python3

from random import choices, randrange

import pyglet

import parameters as p
from game import camera, util, player, map_object, resources as r, npc, effect, hud, map

weights = [1, 20, 3, 1, 0]
traversability = {r.red_tile: False, r.green_tile: True, r.blue_tile: False, r.black_tile: False, r.sand_tile: True}

map_obj = map.Map(tile_imgs=r.tile_imgs, weights=weights, map_tile_width=p.MAP_TILE_WIDTH,
                  map_tile_height=p.MAP_TILE_HEIGHT)

game_window = pyglet.window.Window(width=p.WINDOW_WIDTH, height=p.WINDOW_HEIGHT, resizable=True, caption=p.GAME_NAME)
game_window.set_maximum_size(p.MAP_PIXEL_WIDTH, p.MAP_PIXEL_HEIGHT)
game_window.set_minimum_size(*[p.TILE_SIZE * 3] * 2)
game_window.set_icon(r.player_image)

main_batch = pyglet.graphics.Batch()

background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)
interface_layers = [pyglet.graphics.OrderedGroup(x) for x in (2, 3)]

fps_label = pyglet.text.Label(text=f"FPS : {0}", x=p.WINDOW_WIDTH - 30, y=p.WINDOW_HEIGHT - 10, anchor_x='center',
                              anchor_y='center', font_size=10, batch=main_batch, group=interface_layers[1])

game_hud = hud.HUD(hud_batch=main_batch, hud_groups=interface_layers, inv_slot_img=r.inventory_slot,
                   inv_select_img=r.inventory_select, inv_current_img=r.inventory_selected, middle=p.WINDOW_HALF_WIDTH,
                   item_imgs=r.attack_symbols)

tile_objs = []
env_obj_dict = {}


def get_max_dims(img_list):
    return [max([getattr(img, attr) for img in img_list]) for attr in ("width", "height")]


max_width_env_imgs, max_height_env_imgs = get_max_dims(r.env_imgs)

for i in range(p.MAP_TILE_HEIGHT):
    for j in range(p.MAP_TILE_WIDTH):
        x, y = util.tiles_to_pixels(i, j)
        tile = map_obj.tile_map[i][j]
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

for _ in range(10 * p.MAP_TILE_SCALE):
    pos = generate_position()
    ai_characters.append(
        npc.NPC(img=choices(r.ai_char_imgs)[0], map_x=pos[0], map_y=pos[1], group=foreground, batch=main_batch))


def make_ai_chars_dict(ai_chars_list):
    return {(int(char.x), int(char.y)): char for char in ai_chars_list}


max_width_ai_chars, max_height_ai_chars = get_max_dims(r.ai_char_imgs)

protagonist = player.Player(
    c_img=r.player_image, l_img=r.player_left_image, r_img=r.player_right_image,
    c_ani=r.player_animation, l_ani=r.player_left_animation, r_ani=r.player_right_animation,
    x=game_window.width // 2, y=game_window.height // 2, map_x=p.MAP_PIXEL_HALF_WIDTH, map_y=p.MAP_PIXEL_HALF_HEIGHT,
    batch=main_batch, group=foreground)

for handler in [item for row in [getattr(obj, "event_handlers") for obj in (protagonist, game_hud)] for item in row]:
    game_window.push_handlers(handler)

# @game_window.event
# def on_resize(width, height):
#     cam.apply(protagonist)

animations = []


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


def update(dt):
    cam.update(protagonist)

    if protagonist.effect:
        try:
            new_ani = effect.Effect(img=r.attack_animations[protagonist.current], x=protagonist.effect_x,
                                    y=protagonist.effect_y, group=foreground, batch=main_batch)
            cam.initialise(new_ani)
            animations.append(new_ani)
        except AttributeError or TypeError:
            pass
        protagonist.effect = False

    protagonist.current = game_hud.current

    for dy_obj in [protagonist] + ai_characters:
        dy_obj.update_obj(dt)
        dy_obj.check_map_bounds(p.MAP_PIXEL_WIDTH, p.MAP_PIXEL_HEIGHT)

    # ai_chars_dict = make_ai_chars_dict(ai_characters)

    for ani in animations:
        if ani.remove:
            ani.delete()
            animations.remove(ani)

        # width = int(ani.half_width + max_width_ai_chars // 2)
        # height = int(ani.half_height + max_height_ai_chars // 2)
        #
        # print([key for key in ai_chars_dict.keys()])
        # print([int(ani.map_x) + xx for xx in range(-width, width + 1)])
        # exit()
        #
        # for x in [int(ani.map_x) + xx for xx in range(-width, width + 1)]:
        #     for y in [int(ani.map_y) + yy for yy in range(-height, height + 1)]:
        #         try:
        #             # print(ai_chars_dict)
        #             target = ai_chars_dict[(x, y)]
        #             print(target)
        #             target.check_attack(ani)
        #         except KeyError:
        #             pass

    for dude in ai_characters:
        for ani in animations:
            dude.check_attack(ani)
        if dude.remove:
            dude.delete()
            ai_characters.remove(dude)

    protagonist.check_traversability(tile_objs, env_obj_dict, max_width_env_imgs, max_height_env_imgs)

    for object_ in tile_objs + list(env_obj_dict.values()) + ai_characters + animations:
        cam.apply(object_)

    # game_hud.update_obj()

    fps = pyglet.clock.get_fps()
    fps_label.text = f"FPS: {int(fps)}"


def main():
    pyglet.clock.schedule_interval(update, 1 / p.UPS)
    pyglet.app.run()


if __name__ == "__main__":
    main()
