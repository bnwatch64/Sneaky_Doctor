# Game Constants
FRAMERATE = 30
BLOCK_SIZE = 30
GAME_SIZE = [
    32 * BLOCK_SIZE,
    int(23.7 * BLOCK_SIZE),
]  # Calculate game size by perspective and block size
REAL_GAME_SIZE = (32 * BLOCK_SIZE, 31 * BLOCK_SIZE)
BAR_HEIGHT = 100
SCREEN_SIZE = [GAME_SIZE[0], GAME_SIZE[1] + 2 * BAR_HEIGHT]
WALL_HEIGHT = int(round(2.7 * BLOCK_SIZE))
PLAYER_SIZE = (
    2 * BLOCK_SIZE,
    int(round(2.2 * BLOCK_SIZE)),
)  # Always keeps 200x220 ratio
ENEMY_SIZE = (
    int(round(1.5 * BLOCK_SIZE)),
    int(round(2.4 * BLOCK_SIZE)),
)  # Always keeps 62x100 ratio
FONT_SIZE = 50
BUTTON_SIZE = (30, 30)
ICON_SIZE = (40, 40)

PROTECT_DURATION = 2.0  # Number of seconds player is protected if mask used
DYING_DURATION = 2.0  # Number of seconds dying animation is played
ENEMY_SAMPLES_COUNT = 4  # Number of different enemy assets
PLAYER_SPEED = 5  # Keep lower than BLOCK_SIZE
MAX_NPC_SPEED = 7
ANIMATION_REFRESH = 3
X_PADDING = 20
NUM_LEVELS = 10
FONT_SIZE_BOTTOM_BAR = 40
FLOOR_COLOR = (155, 188, 160)
BAR_COLOR = (40, 40, 40)

ASSETS_LOCATION = "assets"
LEVEL_LOCATION = "levels"
SAVEFILE_NAME = "save.json"
