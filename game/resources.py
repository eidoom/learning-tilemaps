import pyglet

pyglet.resource.path = ['resources']
pyglet.resource.reindex()


def centre_image_horizontally(image):
    image.anchor_x = image.width // 2


def centre_image(image):
    centre_image_horizontally(image)
    image.anchor_y = image.height // 2


def generate_walking_animation(*files, walk_animation_speed=0.1):
    imgs = [pyglet.resource.image(file) for file in files]
    for img in imgs:
        centre_image(img)
    return imgs[0], pyglet.image.Animation.from_image_sequence(imgs + [imgs[0]], walk_animation_speed)


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

if __name__ == "__main__":
    exit()
