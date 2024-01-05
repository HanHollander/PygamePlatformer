import copy
import pygame as pg

import config as c
import elements

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
        pixel_density = self.viewport.screen_size.x / self.viewport.camera.width

        new_camera_width = event.w / pixel_density
        new_camera_height = event.h / pixel_density
    
        self.update_viewport(Viewport(
            pg.Rect(self.viewport.camera.x - (new_camera_width - self.viewport.camera.width) / 2,
                    self.viewport.camera.y - (new_camera_height - self.viewport.camera.height) / 2,
                    new_camera_width, new_camera_height), pg.Vector2(event.w, event.h)))

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
    pass