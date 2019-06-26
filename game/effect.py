from game import positional_object


class Effect(positional_object.PositionalObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.remove = False

    def on_animation_end(self):
        self.remove = True
