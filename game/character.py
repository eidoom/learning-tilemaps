from game import positional_object, util


class Character(positional_object.PositionalObject):
    def __init__(self, mvmt_spd, affinity, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.movement_speed = mvmt_spd
        self.affinity = affinity

        tmp1 = {"ice": "fire"}
        tmp2 = {value: key for key, value in tmp1.items()}
        self.affinity_wheel = {**tmp1, **tmp2, "electricity": "electricity"}

    def check_map_bounds(self, map_width, map_height):
        min_x = self.half_width
        min_y = self.half_height
        max_x = map_width - self.half_width
        max_y = map_height - self.half_height
        if self.map_x < min_x:
            self.map_x = min_x
        elif self.map_x > max_x:
            self.map_x = max_x
        if self.map_y < min_y:
            self.map_y = min_y
        elif self.map_y > max_y:
            self.map_y = max_y

    # def find_near_objs_centre_anchor(self, obj_dict, obj_max_width, obj_max_height):
    #     width = (self.half_width + obj_max_width // 2) // self.col_res
    #     height = (self.half_height + obj_max_height // 2) // self.col_res
    #
    #     objs = []
    #
    #     for x in [int(self.col_x()) + xx for xx in range(-width, width + 1)]:
    #         for y in [int(self.col_y()) + yy for yy in range(-height, height + 1)]:
    #             try:
    #                 objs.append(obj_dict[(x, y)])
    #             except KeyError:
    #                 pass
    #
    #     return objs

    def find_near_objs_bottom_left_anchor(self, obj_dict, obj_max_width, obj_max_height):
        objs = []

        for x in [int(self.col_x()) + xx for xx in
                  range(-int(self.half_width + obj_max_width) // self.col_res,
                        self.half_width // self.col_res + 1)]:
            for y in [int(self.col_y()) + yy for yy in
                      range(-int(self.half_height + obj_max_height) // self.col_res,
                            self.half_height // self.col_res + 1)]:
                try:
                    objs.append(obj_dict[(x, y)])
                except KeyError:
                    pass

        return objs

    def check_traversability(self, tile_objs, env_obj_dict, max_width, max_height):

        centre_i, centre_j = util.pixels_to_tiles(self.map_x, self.map_y)

        tiles = []

        def add_tile(i_, j_):
            try:
                tiles.append(tile_objs[util.nested_ref_to_list_ref(i_, j_)])
            except IndexError:
                pass

        for i in [centre_i + ii for ii in (-1, 1)]:
            for j in [centre_j + jj for jj in range(-1, 2)]:
                add_tile(i, j)

        for j in [centre_j + jj for jj in (-1, 1)]:
            add_tile(centre_i, j)

        env_objs = self.find_near_objs_bottom_left_anchor(env_obj_dict, max_width, max_height)

        for obj in tiles + env_objs:
            if not obj.traversable:
                left = obj.map_x - self.half_width
                right = obj.map_x + obj.width + self.half_width
                bottom = obj.map_y - self.half_height
                top = obj.map_y + obj.height + self.half_height

                if left < self.map_x < right and bottom < self.map_y < top:

                    border = 10
                    if bottom + border < self.map_y < top - border:
                        if self.map_x < obj.map_x + obj.half_width:
                            self.map_x = left
                        elif self.map_x > obj.map_x + obj.half_width:
                            self.map_x = right

                    elif left + border < self.map_x < right - border:
                        if self.map_y < obj.map_y + obj.half_height:
                            self.map_y = bottom
                        elif self.map_y > obj.map_y + obj.half_height:
                            self.map_y = top

    def check_attack(self, attack):
        if attack.affinity is self.affinity_wheel[self.affinity] and self.check_collision(attack):
            self.remove = True


if __name__ == "__main__":
    exit()
