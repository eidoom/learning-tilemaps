from random import choices, randrange

from game import character


class NPC(character.Character):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.max_counter = 3000
        self.counter = randrange(self.max_counter)

    def choose_direction(self):
        lst = [1] * 4
        weights = [lst[:i] + [4] + lst[i:] for i in range(5)] + [[1] * 5]

        if 0 < self.counter < 500:
            return weights[0]
        elif 500 < self.counter < 1000:
            return weights[1]
        elif 1000 < self.counter < 1500:
            return weights[2]
        elif 1500 < self.counter < 2000:
            return weights[3]
        elif 2000 < self.counter < 2500:
            return weights[4]
        else:
            return weights[5]

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
