import pygame as pg

import graphics

debug = {}
font = graphics.f_DEBUG
font_size = graphics.c_f_DEBUG_SIZE
x = 0
y0 = 0

def display_debug(surface: pg.Surface) :
    i = 0
    for (key, value) in debug.items():
        surface.blit(font.render(key + ": " + str(value), False, graphics.c_WHITE), (x, y0 + i * font_size))
        i += 1
    debug.clear()