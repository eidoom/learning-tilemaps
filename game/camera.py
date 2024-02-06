from game import util


class Camera:
    def __init__(self, window, map_width, map_height, batch):
        # Camera position is coordinate of bottom left of visible rectangle.
        self.x = 0
        self.y = 0
        self.win_len_x = window.width
        self.win_len_y = window.height
        self.map_len_x = map_width
        self.map_len_y = map_height
        self.batch = batch
        self.active_tiles = []
        self.i, self.j = util.pixels_to_tiles(self.x, self.y)
        self.last_i, self.last_j = self.i, self.j

        self.out_view_i = [-1, window.tile_height + 1]
        self.out_view_j = [-1, window.tile_width + 1]
        self.in_view_i = [0, window.tile_height]
        self.in_view_j = [0, window.tile_width]

        self.out_view_i_range = self.out_view_i.copy()
        self.out_view_i_range[1] += 1
        self.out_view_j_range = self.out_view_j.copy()
        self.out_view_j_range[1] += 1
        self.in_view_i_range = self.in_view_i.copy()
        self.in_view_i_range[1] += 1
        self.in_view_j_range = self.in_view_j.copy()
        self.in_view_j_range[1] += 1

    def initialise(self, target):
        target.map_x = target.x + self.x
        target.map_y = target.y + self.y

    def apply(self, target):
        target.x = target.map_x - self.x
        target.y = target.map_y - self.y

    def set_coord(self, coord, target):
        the_coord = getattr(self, coord)
        map_coord = getattr(target, f"map_{coord}")
        win_lim = getattr(self, f"win_len_{coord}")
        map_lim = getattr(self, f"map_len_{coord}")
        if getattr(target, f"map_{coord}") < win_lim // 2:
            setattr(self, coord, 0)
            setattr(target, coord, map_coord - the_coord)
        elif map_coord > map_lim - win_lim // 2:
            setattr(self, coord, map_lim - win_lim)
            setattr(target, coord, map_coord - the_coord)
        else:
            setattr(self, coord, map_coord - win_lim // 2)

    def activate_tiles(self, tiles, i_range, j_range, active):
        batch = self.batch if active else None
        for i_ in [self.i - a for a in i_range]:
            for j_ in [self.j + b for b in j_range]:
                try:
                    tile_ = tiles[util.nested_ref_to_list_ref(i_, j_)]
                    tile_.batch = batch
                    if active:
                        self.active_tiles.append(tile_)
                    else:
                        try:
                            self.active_tiles.remove(tile_)
                        except ValueError:
                            pass
                except IndexError:
                    pass

    def update(self, target, tiles):
        self.set_coord("x", target)
        self.set_coord("y", target)

        self.last_i, self.last_j = self.i, self.j
        self.i, self.j = util.pixels_to_tiles(self.x, self.y)

        if self.i > self.last_i:
            self.activate_tiles(
                tiles, (self.out_view_i[1],), range(*self.out_view_j_range), False
            )
            self.activate_tiles(
                tiles, (self.in_view_i[0],), range(*self.in_view_j_range), True
            )
        elif self.i < self.last_i:
            self.activate_tiles(
                tiles, (self.out_view_i[0],), range(*self.out_view_j_range), False
            )
            self.activate_tiles(
                tiles, (self.in_view_i[1],), range(*self.in_view_j_range), True
            )

        if self.j > self.last_j:
            self.activate_tiles(
                tiles, range(*self.out_view_i_range), (self.out_view_j[0],), False
            )
            self.activate_tiles(
                tiles, range(*self.in_view_i_range), (self.in_view_j[1],), True
            )
        elif self.j < self.last_j:
            self.activate_tiles(
                tiles, range(*self.out_view_i_range), (self.out_view_j[1],), False
            )
            self.activate_tiles(
                tiles, range(*self.in_view_i_range), (self.in_view_j[0],), True
            )


if __name__ == "__main__":
    exit()
