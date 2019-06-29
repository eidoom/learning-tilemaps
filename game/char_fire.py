from game import npc, resources as r


class CharFire(npc.NPC):
    def __init__(self, *args, **kwargs):
        super().__init__(img=r.char_enemy_ranged_fire, mvmt_spd=50, affinity="fire", *args, **kwargs)


if __name__ == "__main__":
    exit()
