import pyglet

pyglet.resource.path = ['resources']
pyglet.resource.reindex()


def centre_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def import_and_centre(file_name):
    image = pyglet.resource.image(file_name)
    centre_image(image)
    return image


def generate_walking_animation(*files, walk_animation_speed=0.1):
    imgs = [import_and_centre(file) for file in files]
    return imgs[0], \
           pyglet.image.Animation.from_image_sequence(sequence=imgs + [imgs[0]], period=walk_animation_speed, loop=True)


def generate_effect(file):
    grid = pyglet.resource.image(file)
    images = pyglet.image.ImageGrid(image=grid, rows=2, columns=8)
    for image in images:
        centre_image(image)
    return pyglet.image.Animation.from_image_sequence(sequence=images, period=0.07, loop=False)


def generate_attack(file):
    grid = pyglet.resource.image(file)
    images = pyglet.image.ImageGrid(image=grid, rows=2, columns=8)
    for image in images:
        centre_image(image)
    animation = pyglet.image.Animation.from_image_sequence(sequence=images, period=0.07, loop=False)
    symbol = pyglet.image.Animation.from_image_sequence(sequence=images, period=0.07, loop=True)
    return symbol, animation


red_tile = pyglet.resource.image("tile_red.png")
green_tile = pyglet.resource.image("tile_green.png")
blue_tile = pyglet.resource.image("tile_blue.png")
black_tile = pyglet.resource.image("tile_black.png")
sand_tile = pyglet.resource.image("tile_sand.png")

tile_imgs = [red_tile, green_tile, blue_tile, black_tile, sand_tile]

tree = pyglet.resource.image("env_tree.png")
tree_frozen = pyglet.resource.image("env_tree_frozen.png")
stone = pyglet.resource.image("env_stone.png")

env_imgs = [tree, stone]

player_image, player_animation = generate_walking_animation("player.png", "player_2.png")
player_left_image, player_left_animation = generate_walking_animation("player_left.png", "player_left_2.png")
player_right_image, player_right_animation = generate_walking_animation("player_right.png", "player_right_2.png")

char_npc_air = import_and_centre("char_npc_air.png")
char_enemy_melee_green = import_and_centre("char_enemy_melee_green.png")
char_enemy_ranged_fire = import_and_centre("char_enemy_ranged_fire.png")

ai_char_imgs = [char_npc_air]

fire_symbol, fire_animation = generate_attack('fire_attack.png')
electricity_symbol, electricity_animation = generate_attack('electricity_attack.png')
ice_symbol, ice_animation = generate_attack('ice_attack.png')

attack_animations = [fire_animation, electricity_animation, ice_animation]
attack_symbols = [fire_symbol, electricity_symbol, ice_symbol]

inventory_slot = import_and_centre("inventory_slot.png")
inventory_select = import_and_centre("inventory_slot_select.png")
inventory_selected = import_and_centre("inventory_slot_selected.png")

smoke = generate_effect('smoke.png')

if __name__ == "__main__":
    exit()
