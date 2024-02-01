import pygame as pg

from pynkie.elements import SpriteElement

# physics sprite

class PhysicsElement(SpriteElement):

    def __init__(self, 
                 pos: tuple[int, int], 
                 img: pg.Surface):
        SpriteElement.__init__(self, pos, img)
        self.mask = pg.mask.from_surface(self.image)
        self.old_rect = self.rect.copy()
