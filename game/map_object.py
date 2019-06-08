from game import positional_object


class MapObject(positional_object.PositionalObject):
    def __init__(self, traversable=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.traversable = traversable


if __name__ == "__main__":
    exit()
