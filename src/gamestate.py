from elements import *
import actions
import config as c


class Game:

    def __init__(self) -> None:
        pass

    def update(self, elements: ElementList) -> None:
        pass

    def on_key_down(self, event: pg.event.Event, elements: ElementList):
            if event.key == pg.K_q:
                 actions.quit(event, elements, self)