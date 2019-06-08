from random import choices, randrange

from game import character


class NPC(character.Character):
    def __init__(self, *args, **kwargs):
        super().__init__(mvmt_spd=50, *args, **kwargs)

        self.max_counter = 3000
        self.counter = randrange(self.max_counter)

    def choose_direction(self):
        if 0 < self.counter < 500:
            return [1, 1, 4, 1, 1]
        elif 500 < self.counter < 1000:
            return [1, 1, 1, 4, 1]
        elif 1000 < self.counter < 1500:
            return [1, 1, 1, 1, 4]
        elif 1500 < self.counter < 2000:
            return [4, 1, 1, 1, 1]
        elif 2000 < self.counter < 2500:
            return [1, 4, 1, 1, 1]
        else:
            return [1] * 5

    def update_obj(self, dt):
        direction = choices(range(0, 5), weights=self.choose_direction())[0]
        if direction == 0:
            self.map_x -= self.movement_speed * dt
        elif direction == 1:
            self.map_x += self.movement_speed * dt
        elif direction == 2:
            self.map_y += self.movement_speed * dt
        elif direction == 3:
            self.map_y -= self.movement_speed * dt

        self.counter = (self.counter + 1) % self.max_counter


if __name__ == "__main__":
    exit()
