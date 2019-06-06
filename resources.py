import pyglet

pyglet.resource.path = ['resources']
pyglet.resource.reindex()


def centre_image_horizontally(image):
    image.anchor_x = image.width // 2


def centre_image(image):
    centre_image_horizontally(image)
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

# centre_image_horizontally(tree)
# centre_image_horizontally(stone)
