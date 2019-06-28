import pyglet


class HUD:
    def __init__(self, hud_batch, hud_group, inv_slot_img, inv_select_img, inv_current_img, middle):
        self.hud_batch = hud_batch
        self.hud_group = hud_group
        self.inv_slot_img = inv_slot_img
        self.inv_select_img = inv_select_img
        self.inv_current_img = inv_current_img
        self.middle = middle

        self.offset = 20
        self.slot_width = self.inv_slot_img.width

        self.key_handler = pyglet.window.key.KeyStateHandler()
        self.event_handlers = [self, self.key_handler]

        self.slots = [self.make_slot(index, self.inv_slot_img) for index in range(3)]

        self.current = 1
        self.assign_slot(self.current, self.inv_current_img)

    def make_slot(self, number, img):
        return pyglet.sprite.Sprite(
            img=img, x=self.middle + range(-1, 2)[number] * self.slot_width, y=self.offset,
            batch=self.hud_batch, group=self.hud_group)

    def assign_slot(self, number, img):
        self.slots[number] = self.make_slot(number, img)

    def on_key_press(self, symbol, modifiers):
        if symbol is pyglet.window.key._1:
            num = 0
        if symbol is pyglet.window.key._2:
            num = 1
        if symbol is pyglet.window.key._3:
            num = 2
        self.assign_slot(num, self.inv_select_img)

    def on_key_release(self, symbol, modifiers):
        self.assign_slot(self.current, self.inv_slot_img)
        if symbol is pyglet.window.key._1:
            self.current = 0
        if symbol is pyglet.window.key._2:
            self.current = 1
        if symbol is pyglet.window.key._3:
            self.current = 2
        self.assign_slot(self.current, self.inv_current_img)

    # def update_obj(self):
