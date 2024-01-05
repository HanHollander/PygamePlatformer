import time

import pygame as pg

import config
import events
import setup
import debug
from model import *
from elements import *
from view import View

def run():
    # setup mouse
    pg.mouse.set_visible(False)

    # setup screen and clock
    display, screen = setup.setup_screen()
    clock = pg.time.Clock()

    # Background layers

    # setup game
    view = View()
    game = Game(view)

    # Foreground layers
    # foreground_groups = setup.setup_foreground()

    # run main loop
    main_loop(display, screen, clock, view, game)


def main_loop(display: pg.Surface, screen: pg.Surface, clock: pg.time.Clock, view: View, game: Game):
    prev_time = time.time()
    dt = 0  # delta time [s]
    while True:
        # handle events
        # update the state of elements based on events/player triggers
        events.handle_events(game)
        
        # update game
        game.update(dt)

        # draw elements
        view.draw(screen)

        # debug info
        if config.DEBUG_INFO: debug.display_debug(screen)
        
        # update screen
        display.blit(screen, (0, 0))
        pg.display.flip()

        # tick
        clock.tick(config.FRAMERATE)

        # delta time
        now = time.time()
        dt = now - prev_time
        prev_time = now