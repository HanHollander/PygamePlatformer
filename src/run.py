import pygame as pg

import config
import events
import setup
from gamestate import Game
from elements import Element, ElementList

def run():
    # setup mouse
    pg.mouse.set_visible(False)

    # setup screen and clock
    display, screen = setup.setup_screen()
    clock = pg.time.Clock()

    # setup elements and groups - NB order is also drawing order
    elements = ElementList()
    setup.setup_elements(elements, screen)

    for element in elements:
        print(str(element))

    # setup game
    game = Game()

    # run main loop
    main_loop(display, screen, clock, elements, game)


def main_loop(display: pg.Surface, screen: pg.Surface, clock: pg.time.Clock, elements: ElementList, game: Game):
    while True:
        # handle events
        # update the state of elements based on events/player triggers
        events.handle_events(elements, game)
        
        # update elements
        # update the state of elements based on 
        for element in elements:
            element.update(elements, game)
        
        # update game
        game.update(elements)

        # draw elements
        for element in elements:
            element.draw(screen)
        
        # update screen
        display.blit(screen, (0, 0))
        pg.display.flip()

        # tick
        clock.tick(config.FRAMERATE)