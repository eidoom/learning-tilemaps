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
