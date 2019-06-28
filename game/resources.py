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
    imgs = [pyglet.resource.image(file) for file in files]
    for img in imgs:
        centre_image(img)
    return imgs[0], \
           pyglet.image.Animation.from_image_sequence(sequence=imgs + [imgs[0]], period=walk_animation_speed, loop=True)


red_tile = pyglet.resource.image("tile_red.png")
green_tile = pyglet.resource.image("tile_green.png")
blue_tile = pyglet.resource.image("tile_blue.png")
black_tile = pyglet.resource.image("tile_black.png")
sand_tile = pyglet.resource.image("tile_sand.png")

tile_imgs = [red_tile, green_tile, blue_tile, black_tile, sand_tile]

tree = pyglet.resource.image("env_tree.png")
stone = pyglet.resource.image("env_stone.png")

env_imgs = [tree, stone]

player_image, player_animation = generate_walking_animation("player.png", "player_2.png")
player_left_image, player_left_animation = generate_walking_animation("player_left.png", "player_left_2.png")
player_right_image, player_right_animation = generate_walking_animation("player_right.png", "player_right_2.png")

char_npc_air = pyglet.resource.image("char_npc_air.png")

explosion_images_image = pyglet.resource.image('explosion.png')
explosion_images = pyglet.image.ImageGrid(image=explosion_images_image, rows=2, columns=8)
# explosion_images = explosion_images.get_texture_sequence()
for img in explosion_images:
    centre_image(img)
# explosion_img = explosion_images[4]
explosion_animation = pyglet.image.Animation.from_image_sequence(sequence=explosion_images, period=0.07, loop=False)
explosion_symbol = pyglet.image.Animation.from_image_sequence(sequence=explosion_images, period=0.07, loop=True)

interactions = [None, explosion_animation, None]

inventory_slot = import_and_centre("inventory_slot.png")
inventory_select = import_and_centre("inventory_slot_select.png")
inventory_selected = import_and_centre("inventory_slot_selected.png")

if __name__ == "__main__":
    exit()
