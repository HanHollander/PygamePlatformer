import sys
import pygame as pg
from elements import *
from gamestate import Game

def nop(event: pg.event.Event, elements: ElementList, game: Game):
    pass

def quit(event: pg.event.Event, elements: ElementList, game: Game):
    pg.quit()
    sys.exit()