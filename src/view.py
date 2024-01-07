import copy
from typing import Any, Iterable, Union
import pygame as pg
from pygame.sprite import AbstractGroup

import elements
import graphics

class Viewport:

    def __init__(self, camera: pg.Rect, screen_size: pg.Vector2) -> None:
        self.camera = camera
        self.screen_size = screen_size

class View(pg.sprite.Group):
    
    def __init__(self, viewport: Viewport):
        pg.sprite.Group.__init__(self)
        self.viewport: Viewport
        self.background: pg.Surface
        self.view_surface: pg.Surface
        self.center_element: elements.Element = None
        self.update_viewport(viewport)

    def on_window_resize(self, event: pg.event.Event) -> None:
        old_window_ratio = self.viewport.screen_size.x / self.viewport.screen_size.y
        new_window_ratio = event.w / event.h

        new_camera: pg.Rect = copy.copy(self.viewport.camera)
        if new_window_ratio > old_window_ratio:
            new_camera.width = new_camera.height * new_window_ratio
            new_camera.x -= (new_camera.width - self.viewport.camera.width) / 2
        else:
            new_camera.height = new_camera.width / new_window_ratio
            new_camera.y -= (new_camera.height - self.viewport.camera.height) / 2
    
        self.update_viewport(Viewport(new_camera, pg.Vector2(event.w, event.h)))

    def center_camera(self) -> None:
        if self.center_element is not None:
            self.viewport.camera.x = self.center_element.rect.centerx - self.viewport.camera.width / 2
            self.viewport.camera.y = self.center_element.rect.centery - self.viewport.camera.height / 2


    def update_viewport(self, new_viewport: Viewport) -> None:
        self.viewport = new_viewport
        self.background = pg.Surface(size=(self.viewport.camera.width, self.viewport.camera.height))
        self.background.fill((20, 20, 20))
        self.view_surface = pg.Surface(size=(self.viewport.camera.width, self.viewport.camera.height))


    # override
    def draw(self, screen: pg.Surface):
        self.center_camera()

        self.view_surface.blit(self.background, pg.Rect(0, 0, self.viewport.camera.width, self.viewport.camera.height), None, 0)
        # - reposition camera
        #   - make it center
        #   - free cam mode
        #   - follow viking?
        # - Z order
        # - scale

        for spr in self.sprites():
            if spr.rect.colliderect(self.viewport.camera):
                target_rect = pg.Rect(spr.rect.x - self.viewport.camera.x, spr.rect.y - self.viewport.camera.y,
                                    spr.rect.width, spr.rect.height)
                self.spritedict[spr] = self.view_surface.blit(spr.image, target_rect, None, 0)

        # Scale the view surface to the dimensions of the screen and blit directly
        pg.transform.scale(self.view_surface, self.viewport.screen_size, screen)

    def __str__(self):
        return str(self.type) + ": " + pg.sprite.Group.__str__(self)

class GUIView(pg.sprite.Group):
    
    def __init__(self, *sprites: Any | AbstractGroup | Iterable) -> None:
        super().__init__(*sprites)

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