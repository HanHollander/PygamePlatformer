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
    setup_platform(elements, screen)
    setup_cursor(elements, screen)

def setup_background(elements: ElementList, screen: pg.Surface):    
    group = GroupElement(screen, GroupType.MISC)
    background = pg.Surface(
        size=(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
    )
    background.fill((20, 20, 20))
    group.add(SpriteElement(
        pos=(0, 0),
        img=background
    ))
    elements.append(group)

def setup_viking(elements: ElementList, background: pg.Surface):
    group = GroupElement(background, GroupType.MISC)
    group.add(PhysicsSprite(
        pos=(100, 50),
        max_velocity=1.0,
        velocity=0.0,
        direction=0.0,
        acceleration=0.0,
        mass=1,
        img=graphics.img_viking
    ))
    elements.append(group)

def setup_platform(elements: ElementList, background: pg.Surface):
    group = GroupElement(background, GroupType.MISC)
    platform = pg.Surface(
        size=(150, 10)
    )
    platform.fill((255, 255, 255))
    group.add(SpriteElement(
        pos=(20, 100),
        img=platform
    ))
    elements.append(group)

def setup_cursor(elements: ElementList, background: pg.Surface):
    group = GroupElement(background, GroupType.CURSOR)
    group.add(Cursor(
        pos=(20, 240 - graphics.img_cursor.get_size()[1] / 2),
        img=graphics.img_cursor
    ))
    elements.append(group)
