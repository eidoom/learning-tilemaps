from game import positional_object


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

    def check_attack(self, attack):
        if attack.affinity is self.affinity_wheel[self.affinity] and self.check_collision(attack):
            self.remove = True


if __name__ == "__main__":
    exit()
