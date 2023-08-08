import pygame as pg

import config
import events
import setup
from model import *
from elements import *

def run():
    # setup mouse
    pg.mouse.set_visible(False)

    # setup screen and clock
    display, screen = setup.setup_screen()
    clock = pg.time.Clock()

    # setup game
    world_group = GroupElement(screen, GroupType.MISC)
    game = Game(world_group)

    # run main loop
    main_loop(display, screen, clock, world_group, game)


def main_loop(display: pg.Surface, screen: pg.Surface, clock: pg.time.Clock, world_group: GroupElement, game: Game):
    while True:
        # handle events
        # update the state of elements based on events/player triggers
        events.handle_events(game)
        
        # update game
        game.update()

        # draw elements
        world_group.draw(screen)
        
        # update screen
        display.blit(screen, (0, 0))
        pg.display.flip()

        # tick
        clock.tick(config.FRAMERATE)