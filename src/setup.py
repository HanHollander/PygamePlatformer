import pygame as pg

import config
import graphics
import actions
from elements import *


def setup_screen():
    size = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
    flags = pg.NOFRAME | pg.SCALED | pg.HWSURFACE | pg.DOUBLEBUF
    display = pg.display.set_mode(size, flags, vsync=1)
    pg.display.set_caption("gmtk2023test")
    screen = pg.Surface(display.get_size())
    screen.fill(graphics.c_BLACK)

    return display, screen

def setup_elements(elements: ElementList, screen: pg.Surface):
    setup_background(elements, screen)
    setup_viking(elements, screen)
    setup_cursor(elements, screen)

def setup_background(elements: ElementList, screen: pg.Surface):
    background = SurfaceElement(
        pos=(0, 0), 
        size=(config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    elements.append(background)

def setup_viking(elements: ElementList, background: pg.Surface):
    group = GroupElement(background, GroupType.MISC)
    group.add(SpriteElement(
        pos=(100, 50),
        img=graphics.img_viking
    ))
    elements.append(group)

def setup_cursor(elements: ElementList, background: pg.Surface):
    group = GroupElement(background, GroupType.CURSOR)
    group.add(Cursor(
        pos=(20, 240 - graphics.img_cursor.get_size()[1] / 2),
        img=graphics.img_cursor
    ))
    elements.append(group)
