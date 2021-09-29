#!/usr/bin/env python3

from random import choices, randrange

import pyglet

import parameters as p
from game import camera, util, player, map_object, resources as r, char_air, effect, hud, map, char_fire, char_green, \
    window

weights = [0, 10, 1, 0, 0]
traversability = {r.red_tile: False, r.green_tile: True, r.blue_tile: False, r.black_tile: False, r.sand_tile: True}

map_obj = map.Map(tile_imgs=r.tile_imgs, weights=weights, map_tile_width=p.MAP_TILE_WIDTH,
                  map_tile_height=p.MAP_TILE_HEIGHT, tile_size=p.TILE_SIZE)

game_batch = pyglet.graphics.Batch()

game_window = window.GameWindow(caption=p.GAME_NAME, fullscreen=p.FULLSCREEN,
                                max_width=map_obj.width, max_height=map_obj.height,
                                min_size=p.TILE_SIZE * 3, icon=r.player_image, tile_size=p.TILE_SIZE,
                                width=p.WINDOW_WIDTH, height=p.WINDOW_HEIGHT, batch=game_batch, show_fps=p.SHOW_FPS)

background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)
interface_layers = [pyglet.graphics.OrderedGroup(x) for x in (2, 3)]

game_hud = hud.HUD(hud_batch=game_batch, hud_groups=interface_layers, inv_slot_img=r.inventory_slot,
                   inv_select_img=r.inventory_select, inv_current_img=r.inventory_selected,
                   middle=game_window.half_width, item_imgs=r.attack_symbols)

tile_objs = []
env_obj_dict = {}
max_width_env_imgs, max_height_env_imgs = util.get_max_dims(r.env_imgs)

# mvmt_mask = [[traversability[map_obj.get_tile(i, j)] for j in range(p.MAP_TILE_WIDTH)]
#              for i in range(p.MAP_TILE_HEIGHT)]

for i in range(p.MAP_TILE_HEIGHT):
    for j in range(p.MAP_TILE_WIDTH):
        x, y = util.tiles_to_pixels(i, j)
        tile = map_obj.get_tile(i, j)
        tile_objs.append(map_object.MapObject(
            img=tile, traversable=traversability[tile], map_x=x, map_y=y, batch=None, group=background))
        if choices([True, False], weights=[1, 9])[0]:
            obj_x = x + randrange(0, tile.width)
            obj_y = y + randrange(0, tile.height)
            if tile in (r.green_tile,):
                obj = map_object.MapObject(img=r.tree, traversable=False, map_x=obj_x, map_y=obj_y, batch=game_batch,
                                           group=foreground)
            elif tile in (r.sand_tile,):
                obj = map_object.MapObject(img=r.stone, traversable=True, map_x=obj_x, map_y=obj_y, batch=game_batch,
                                           group=foreground)
            try:
                env_obj_dict.update({(obj.col_x(), obj.col_y()): obj})
            except NameError:
                pass

scale = p.TILE_SIZE / r.tile_imgs[0].width

for tile in tile_objs:
    tile.scale = scale

cam = camera.Camera(game_window, map_obj.width, map_obj.height, game_batch)


def generate_position():
    return randrange(0, map_obj.width), randrange(0, map_obj.height)


ai_characters = []

for _ in range(3 * p.MAP_TILE_SCALE):
    x, y = generate_position()
    ai_characters.append(char_air.CharAir(map_x=x, map_y=y, group=foreground, batch=game_batch))
    x, y = generate_position()
    ai_characters.append(char_fire.CharFire(map_x=x, map_y=y, group=foreground, batch=game_batch))
    x, y = generate_position()
    ai_characters.append(char_green.CharGreen(map_x=x, map_y=y, group=foreground, batch=game_batch))

# def make_ai_chars_dict(ai_chars_list):
#     return {(int(char.x), int(char.y)): char for char in ai_chars_list}


# max_width_ai_chars, max_height_ai_chars = util.get_max_dims(r.ai_char_imgs)

protagonist = player.Player(
    c_img=r.player_image, l_img=r.player_left_image, r_img=r.player_right_image,
    c_ani=r.player_animation, l_ani=r.player_left_animation, r_ani=r.player_right_animation,
    x=game_window.width // 2, y=game_window.height // 2, map_x=map_obj.half_width, map_y=map_obj.half_height,
    batch=game_batch, group=foreground)

for handler in [item for row in [getattr(obj, "event_handlers") for obj in (protagonist, game_hud)] for item in row]:
    game_window.push_handlers(handler)

# @game_window.event
# def on_resize(width, height):
#     cam.apply(protagonist)

animations = []

attack_affinities = ["fire", "electricity", "ice"]

cam.update(protagonist, tile_objs)
cam.activate_tiles(tile_objs, range(*cam.in_view_i_range), range(*cam.in_view_j_range), True)


def update(dt):
    if game_window.overlay:
        game_window.overlay.update(dt)

    else:
        if not protagonist.remove:
            cam.update(protagonist, tile_objs)

        if protagonist.effect:
            try:
                new_ani = effect.Effect(
                    img=r.attack_animations[protagonist.current], affinity=attack_affinities[protagonist.current],
                    x=protagonist.effect_x, y=protagonist.effect_y, group=foreground, batch=game_batch)
                cam.initialise(new_ani)
                animations.append(new_ani)
            except AttributeError or TypeError:
                pass
            protagonist.effect = False

        protagonist.current = game_hud.current

        for dy_obj in [protagonist] + ai_characters:
            dy_obj.update_obj(dt)
            dy_obj.check_map_bounds(map_obj.width, map_obj.height)
            dy_obj.check_traversability(tile_objs, env_obj_dict, max_width_env_imgs, max_height_env_imgs)

        # ai_chars_dict = make_ai_chars_dict(ai_characters)

        for ani in animations:
            if ani.remove:
                animations.remove(ani)

        for dude in ai_characters:
            for ani in animations:
                dude.check_attack(ani)
            if dude.remove:
                dude.delete()
                ai_characters.remove(dude)
            if protagonist.check_collision(dude) and not protagonist.remove:
                effect.Effect(img=r.smoke, x=protagonist.x, y=protagonist.y, group=foreground, batch=game_batch)
                protagonist.remove = True
                protagonist.visible = False

        for env_obj in env_obj_dict.values():
            for ani in animations:
                env_obj.check_interaction(ani)

        for object_ in cam.active_tiles + list(env_obj_dict.values()) + ai_characters + animations:
            cam.apply(object_)


def main():
    game_window.open_main_menu()
    pyglet.clock.schedule_interval(update, 1 / p.UPS)
    pyglet.app.run()


if __name__ == "__main__":
    main()
