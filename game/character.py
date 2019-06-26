from game import positional_object, util


class Character(positional_object.PositionalObject):
    def __init__(self, mvmt_spd, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.movement_speed = mvmt_spd
        self.hit = False

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

    def check_attack(self, attack):
        # def generate_hit_box(obj):
        #     init_x = int(obj.x)
        #     init_y = int(obj.y)
        #     for y in range(init_y - obj.half_height, init_y + obj.half_height + 1):
        #         for x in range(init_x - obj.half_width, init_x + obj.half_width + 1):
        #             yield x, y
        #
        # for point in generate_hit_box(self):
        #     if point in generate_hit_box(attack):
        #         self.hit = True
        #         return
        collision_distance = self.radius + attack.radius
        actual_distance = util.distance(self.position, attack.position)
        if actual_distance < collision_distance:
            self.hit = True


if __name__ == "__main__":
    exit()
