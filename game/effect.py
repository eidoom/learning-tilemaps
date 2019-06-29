from game import positional_object


class Effect(positional_object.PositionalObject):
    def __init__(self, affinity=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.affinity = affinity

    def on_animation_end(self):
        self.remove = True
        self.delete()


if __name__ == "__main__":
    exit()
