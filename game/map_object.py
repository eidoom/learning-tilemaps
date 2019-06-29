from game import positional_object, resources


class MapObject(positional_object.PositionalObject):
    def __init__(self, traversable=True, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.traversable = traversable

    def check_interaction(self, other_obj):
        if self.check_collision(other_obj):
            if other_obj.affinity is "ice":
                if self.image is resources.tree:
                    self.image = resources.tree_frozen
                if self.image is resources.stone:
                    self.image = resources.stone_frozen
            if other_obj.affinity is "fire":
                if self.image is resources.tree_frozen:
                    self.image = resources.tree
                if self.image is resources.stone_frozen:
                    self.image = resources.stone


if __name__ == "__main__":
    exit()
