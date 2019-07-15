UPS = 60

GAME_NAME = "Tile map game"

TILE_SIZE = 40
HALF_TILE_SIZE = TILE_SIZE // 2
MAP_TILE_SCALE = 3
MAP_TILE_WIDTH_RATIO = 16
MAP_TILE_HEIGHT_RATIO = 9
MAP_TILE_WIDTH = MAP_TILE_WIDTH_RATIO * MAP_TILE_SCALE
MAP_TILE_HEIGHT = MAP_TILE_HEIGHT_RATIO * MAP_TILE_SCALE
MAP_TILE_HALF_WIDTH = MAP_TILE_WIDTH // 2
MAP_TILE_HALF_HEIGHT = MAP_TILE_HEIGHT // 2

MAP_PIXEL_WIDTH = MAP_TILE_WIDTH * TILE_SIZE
MAP_PIXEL_HEIGHT = MAP_TILE_HEIGHT * TILE_SIZE
MAP_PIXEL_HALF_WIDTH = MAP_PIXEL_WIDTH // 2
MAP_PIXEL_HALF_HEIGHT = MAP_PIXEL_HEIGHT // 2

WINDOW_SCALE = TILE_SIZE
WINDOW_WIDTH_RATIO = 16
WINDOW_HEIGHT_RATIO = 9
WINDOW_WIDTH = WINDOW_WIDTH_RATIO * WINDOW_SCALE
WINDOW_HEIGHT = WINDOW_HEIGHT_RATIO * WINDOW_SCALE
WINDOW_HALF_WIDTH = WINDOW_WIDTH // 2
WINDOW_HALF_HEIGHT = WINDOW_HEIGHT // 2
WINDOW_TILE_WIDTH = WINDOW_WIDTH // TILE_SIZE
WINDOW_TILE_HEIGHT = WINDOW_HEIGHT // TILE_SIZE

if __name__ == "__main__":
    exit()
