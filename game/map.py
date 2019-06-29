from random import choices


class Map:
    def __init__(self, tile_imgs, weights, map_tile_width, map_tile_height):
        self.tile_imgs = tile_imgs

        self.green = self.tile_imgs[1]
        self.blue = self.tile_imgs[2]
        self.sand = self.tile_imgs[4]

        self.weights = weights
        self.map_tile_width = map_tile_width
        self.map_tile_height = map_tile_height

        self.map_tile_half_width = self.map_tile_width // 2
        self.map_tile_half_height = self.map_tile_height // 2

        self.tile_map = [[choices(self.tile_imgs, weights=weights)[0] for _ in range(map_tile_width)] for _ in
                         range(map_tile_height)]
        self.tile_map[self.map_tile_half_height][self.map_tile_half_width] = self.green
        self.tile_map[self.map_tile_half_height][self.map_tile_half_width + 1] = self.green
        self.tile_map[self.map_tile_half_height - 1][self.map_tile_half_width] = self.green
        self.tile_map[self.map_tile_half_height - 1][self.map_tile_half_width + 1] = self.green

        for i in range(self.map_tile_height):
            for j in range(self.map_tile_width):
                if self.tile_map[i][j] == self.blue:
                    try:
                        for ii in (i - 1, i + 1):
                            if not self.tile_map[ii][j] == self.blue:
                                self.tile_map[ii][j] = self.sand
                        for jj in (j - 1, j + 1):
                            if not self.tile_map[i][jj] == self.blue:
                                self.tile_map[i][jj] = self.sand
                    except IndexError:
                        pass


if __name__ == "__main__":
    exit()