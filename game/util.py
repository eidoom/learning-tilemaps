from math import sqrt

import parameters as p


def tiles_to_pixels(i_, j_):
    x_ = j_ * p.TILE_SIZE
    y_ = (p.MAP_TILE_HEIGHT - 1 - i_) * p.TILE_SIZE
    return x_, y_


def pixels_to_tiles(x_, y_):
    i_ = -int((y_ // p.TILE_SIZE) - (p.MAP_TILE_HEIGHT - 1))
    j_ = int(x_ // p.TILE_SIZE)
    return i_, j_


def nested_ref_to_list_ref(i_, j_):
    return i_ * p.MAP_TILE_WIDTH + j_


def distance(point_1=(0, 0), point_2=(0, 0)):
    return sqrt(sum((point_1[i] - point_2[i]) ** 2 for i in range(len(point_1))))


def get_max_dims(img_list):
    return [max([getattr(img, attr) for img in img_list]) for attr in ("width", "height")]


if __name__ == "__main__":
    exit()
