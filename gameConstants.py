# Game Constants
FRAMERATE = 30
BLOCK_SIZE = 30
GAME_SIZE = [
    32 * BLOCK_SIZE,
    int(23.7 * BLOCK_SIZE),
]  # Calculate game size by perspective and block size
REAL_GAME_SIZE = (32 * BLOCK_SIZE, 31 * BLOCK_SIZE)
WALL_HEIGHT = int(round(2.7 * BLOCK_SIZE))
PLAYER_SIZE = (
    2 * BLOCK_SIZE,
    int(round(2.2 * BLOCK_SIZE)),
)  # Always keeps 200x220 ratio
ENEMY_SIZE = (62, 100)  # Always keep 62x100 ratio
BAR_HEIGHT = 100
FONT_SIZE = 50
BUTTON_SIZE = (30, 30)
ICON_SIZE = (40, 40)

ENEMY_SAMPLES_COUNT = 4  # Number of different enemy assets
CHARACTER_SPEED = 7
ANIMATION_REFRESH = 3
X_PADDING = 20
NUM_LEVELS = 10
FONT_SIZE_MASK = 40
FLOOR_COLOR = (200, 200, 200)
BAR_COLOR = (255, 255, 255)

ASSETS_LOCATION = "assets"
LEVEL_LOCATION = "levels"
