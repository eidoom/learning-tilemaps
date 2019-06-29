from game import npc, resources as r


class CharGreen(npc.NPC):
    def __init__(self, *args, **kwargs):
        super().__init__(img=r.char_enemy_melee_green, mvmt_spd=50, affinity="electricity", *args, **kwargs)


if __name__ == "__main__":
    exit()
