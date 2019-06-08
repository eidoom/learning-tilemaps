from game import positional_object


class Character(positional_object.PositionalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == "__main__":
    exit()
