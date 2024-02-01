from pynkie.view import StaticView
import pygame as pg
import graphics
import pynkie.elements as elements

class MyGUIView(StaticView):
    
    def __init__(self) -> None:
        super().__init__()

        self.cursor = Cursor()
        self.add(self.cursor.element)
    
    def on_mouse_motion(self, event: pg.event.Event) -> None:
        self.cursor.on_mouse_motion(event)


class Cursor:
    def __init__(self) -> None:
        sprite = pg.transform.scale_by(graphics.img_cursor.copy(), 4)
        self.element = elements.SpriteElement(
            pos=(20, 240 - sprite.get_size()[1] / 2),
            img=sprite
        )

    def on_mouse_motion(self, event: pg.event.Event) -> None:
        self.element.rect = pg.Rect(
            event.pos, (self.element.rect.w, self.element.rect.h))