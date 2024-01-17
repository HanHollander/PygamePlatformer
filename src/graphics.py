from enum import Enum
import os

import pygame as pg
import config

# colours

c_COLOUR_KEY = (255, 0, 255)  # ff00ff

c_RED = (204, 27, 27)  # cc1b1b
c_DARK_RED = (133, 17, 17)  # 851111

c_WHITE = (255, 255, 255)  # ffffff
c_BLACK = (0, 0, 0)  # 000000
c_DARK_GRAY = (50, 50, 50)  # 333333
c_GRAY = (82, 82, 82)  # 525252
c_LIGHT_GRAY = (148, 148, 148)  # 949494

# fonts

pg.font.init()

f_SMALL = pg.font.SysFont(name="Corbel", size=16, bold=True, italic=False)
c_f_DEBUG_SIZE = 16
f_DEBUG = pg.font.Font(os.path.join("font", "rainyhearts.ttf"), c_f_DEBUG_SIZE)

# cursor

img_cursor = pg.image.load("./img/cursor.png")

# viking

img_viking = pg.image.load("./img/viking.png")