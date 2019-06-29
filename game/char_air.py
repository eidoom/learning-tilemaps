from game import npc, resources as r


class CharAir(npc.NPC):
    def __init__(self, *args, **kwargs):
        super().__init__(img=r.char_npc_air, mvmt_spd=50, affinity="ice", *args, **kwargs)


if __name__ == "__main__":
    exit()
