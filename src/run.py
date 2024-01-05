import pygame as pg

import config
import events
import setup
import debug
from model import *
from elements import *
from view import View, GUIView

def run():
    # setup mouse
    pg.mouse.set_visible(False)

    # setup screen and clock
    display, viewport = setup.setup_screen()
    clock = pg.time.Clock()

    # Background layers

    # setup game
    view = View(viewport)
    game = Game(view)

    # Foreground layers
    gui_view = GUIView()
    gui_layer = UILayer(gui_view)

    # run main loop
    main_loop(display, clock, view, game, gui_view, gui_layer)


def main_loop(display: pg.Surface, clock: pg.time.Clock, view: View, game: Game, gui_view: GUIView, gui_layer: UILayer):
    while True:
        # handle events
        # update the state of elements based on events/player triggers
        events.handle_events(game, gui_layer, view)
        
        # update game
        game.update()

        # draw elements
        view.draw(display)
        gui_view.draw(display)

        # debug info
        if config.DEBUG_INFO: debug.display_debug(display)
        
        # update screen
        pg.display.flip()

        # tick
        debug_dt = clock.tick(config.FRAMERATE)
        debug.debug["DT"] = debug_dt
        debug.debug["FPS"] = 1000 / debug_dt