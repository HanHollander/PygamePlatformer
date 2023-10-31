import pygame as pg

from config import SCREEN_HEIGHT, SCREEN_WIDTH

class ViewPort:

    def __init__(self) -> None:
        self.camera = pg.Rect(20, 20, SCREEN_WIDTH, SCREEN_HEIGHT)

class View(pg.sprite.Group):
    
    def __init__(self):
        pg.sprite.Group.__init__(self)
        self.view_port = ViewPort()
        self.background = pg.Surface(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill((20, 20, 20))


    # override
    def draw(self, screen: pg.Surface):
        screen.blit(self.background, pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), None, 0)
        # - reposition camera
        #   - make it center
        #   - free cam mode
        #   - follow viking?
        # - Z order
        # - scale

        for spr in self.sprites():
            target_rect = pg.Rect(spr.rect.x - self.view_port.camera.x, spr.rect.y - self.view_port.camera.y,
                                  spr.rect.width, spr.rect.height)
            self.spritedict[spr] = screen.blit(spr.image, target_rect, None, 0)

    def __str__(self):
        return str(self.type) + ": " + pg.sprite.Group.__str__(self)