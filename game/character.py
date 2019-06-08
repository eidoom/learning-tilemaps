from game import positional_object


class Character(positional_object.PositionalObject):
    def __init__(self, mvmt_spd, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.movement_speed = mvmt_spd


if __name__ == "__main__":
    exit()
