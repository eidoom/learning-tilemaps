import pyglet


class HUD:
    def __init__(self, hud_batch, hud_groups, inv_slot_img, inv_select_img, inv_current_img, middle, item_imgs):
        self.hud_batch = hud_batch
        self.hud_groups = hud_groups
        self.inv_slot_img = inv_slot_img
        self.inv_select_img = inv_select_img
        self.inv_current_img = inv_current_img
        self.middle = middle
        self.item_imgs = item_imgs

        self.slot_width = self.inv_slot_img.width
        self.offset = self.slot_width // 2

        # self.key_handler = pyglet.window.key.KeyStateHandler()
        # self.event_handlers = [self, self.key_handler]

        self.event_handlers = [self]

        # Currently make_slot() logic requires odd number of slots
        self.number_slots = 3
        self.bar_width = self.number_slots // 2
        self.slots = [self.make_piece(index, self.inv_slot_img, layer=0) for index in range(self.number_slots)]

        self.current = None
        # self.assign_slot(self.current, self.inv_current_img)

        self.num_keys = [getattr(pyglet.window.key, f"_{x}") for x in range(1, self.number_slots + 1)]
        self.slot_dic = {num_key: num for num, num_key in enumerate(self.num_keys)}
        self.sheath = pyglet.window.key.Q

        self.items = [self.make_piece(i, item_img, layer=1) for i, item_img in enumerate(self.item_imgs) if item_img]

    def make_piece(self, number, img, layer=0):
        return pyglet.sprite.Sprite(
            img=img, x=self.middle + range(-self.bar_width, self.bar_width + 1)[number] * self.slot_width,
            y=self.offset, batch=self.hud_batch, group=self.hud_groups[layer])

    def assign_slot(self, number, slot_img):
        self.slots[number] = self.make_piece(number, slot_img, layer=0)

    def assign_item(self, number, item_img):
        self.items[number] = self.make_piece(number, item_img, layer=1)

    def on_key_press(self, symbol, modifiers):
        if symbol is self.sheath:
            self.assign_slot(self.current, self.inv_slot_img)
            self.current = None
        else:
            try:
                self.assign_slot(self.slot_dic[symbol], self.inv_select_img)
            except KeyError:
                pass

    def on_key_release(self, symbol, modifiers):
        if symbol in self.num_keys:
            try:
                self.assign_slot(self.current, self.inv_slot_img)
            except TypeError:
                pass
            self.current = self.slot_dic[symbol]
            self.assign_slot(self.current, self.inv_current_img)

    # def update_obj(self):


if __name__ == "__main__":
    exit()
