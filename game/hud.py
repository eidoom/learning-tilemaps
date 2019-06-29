import pyglet


class HUD:
    def __init__(self, hud_batch, hud_group, inv_slot_img, inv_select_img, inv_current_img, middle):
        self.hud_batch = hud_batch
        self.hud_group = hud_group
        self.inv_slot_img = inv_slot_img
        self.inv_select_img = inv_select_img
        self.inv_current_img = inv_current_img
        self.middle = middle

        self.slot_width = self.inv_slot_img.width
        self.offset = self.slot_width // 2

        # self.key_handler = pyglet.window.key.KeyStateHandler()
        # self.event_handlers = [self, self.key_handler]

        self.event_handlers = [self]

        # Currently make_slot() logic requires odd number of slots
        self.number_slots = 3
        self.bar_width = self.number_slots // 2
        self.slots = [self.make_slot(index, self.inv_slot_img) for index in range(self.number_slots)]

        self.current = 1
        self.assign_slot(self.current, self.inv_current_img)

        self.num_keys = [getattr(pyglet.window.key, f"_{x}") for x in range(1, self.number_slots + 1)]
        self.slot_dic = {num_key: num for num, num_key in enumerate(self.num_keys)}

    def make_slot(self, number, img):
        return pyglet.sprite.Sprite(
            img=img, x=self.middle + range(-self.bar_width, self.bar_width + 1)[number] * self.slot_width,
            y=self.offset, batch=self.hud_batch, group=self.hud_group)

    def assign_slot(self, number, img):
        self.slots[number] = self.make_slot(number, img)

    def on_key_press(self, symbol, modifiers):
        try:
            self.assign_slot(self.slot_dic[symbol], self.inv_select_img)
        except KeyError:
            pass

    def on_key_release(self, symbol, modifiers):
        if symbol in self.num_keys:
            self.assign_slot(self.current, self.inv_slot_img)
            self.current = self.slot_dic[symbol]
            self.assign_slot(self.current, self.inv_current_img)

    # def update_obj(self):
