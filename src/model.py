import math
import pygame as pg

import graphics
import util
import physics
from elements import *
import config
import actions

class Game:

    def __init__(self, world_group: GroupElement):
        self.background = Background()
        world_group.add(self.background.element)
        self.cursor = Cursor()
        world_group.add(self.cursor.element)

        platform = pg.Surface(
            size=(150, 10)
        )
        platform.fill((255, 255, 255))
 
        self.physics_objects = [
            PhysicsObject(
                pos=(100, 50),
                max_velocity=1.0,
                mass=1,
                solid=True,
                gravity=True,
                img=graphics.img_viking
            ),
            PhysicsObject(
                pos=(100, 100),
                max_velocity=0.0,
                mass=1,
                solid=True,
                gravity=False,
                img=platform
            )
        ]
        for physics_object in self.physics_objects:
            world_group.add(physics_object.element)

    def update(self):
        self.background.update()
        self.cursor.update()
        for physics_object in self.physics_objects:
            physics_object.update()

    def on_mouse_motion(self, event: pg.event.Event):
        self.cursor.on_mouse_motion(event)

    def on_key_down(self, event: pg.event.Event, elements: ElementList):
            if event.key == pg.K_q:
                 actions.quit(event, elements, self)


class Background:
    def __init__(self):
        surface = pg.Surface(
            size=(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        )
        surface.fill((20, 20, 20))
        self.element = SpriteElement(
            pos=(0, 0),
            img=surface
        )
    
    def update(self):
        pass

class Cursor:
    def __init__(self):
        self.element = CursorElement(
            pos=(20, 240 - graphics.img_cursor.get_size()[1] / 2),
            img=graphics.img_cursor
        )

    def update(self):
        pass

    def on_mouse_motion(self, event: pg.event.Event):
        self.element.rect = pg.Rect(event.pos, (self.element.rect.w, self.element.rect.h))


class PhysicsObject:
    def __init__(self, pos, max_velocity, mass, solid, gravity, img):
        self.element = SpriteElement(pos, img)

        self.position = physics.Position(pos)  # (px, px)
        self.force_vectors = [physics.c_GRAVITY] if gravity else []
        self.max_velocity = max_velocity  # px/tick
        self.velocity = physics.Vector2(0, 0)  # px/tick
        self.mass = mass  # kg
        self.solid = solid
        self.previous_position = self.position

    def update(self):
        self.previous_position = self.position
        self.apply_force()
        new_rect = pg.Rect(util.get_top_left(self.element.image.get_width(), self.element.image.get_height(), self.position.x, self.position.y), 
                            self.element.image.get_size())

        self.element.rect = new_rect

    def apply_force(self):
        # calculate force
        force_sum_x = 0
        force_sum_y = 0
        for force_vector in self.force_vectors:
            force_sum_x += force_vector.x
            force_sum_y += force_vector.y

        # apply force
        self.velocity.x = min(self.max_velocity, self.velocity.x + force_sum_x / self.mass)
        self.velocity.y = min(self.max_velocity, self.velocity.y + force_sum_y / self.mass)

        # apply velocity
        self.position.xf = self.position.xf + self.velocity.x
        self.position.yf = self.position.yf + self.velocity.y
        self.position.x = math.floor(self.position.xf)
        self.position.y = math.floor(self.position.yf)
        
    
    def restore_previous_position(self):
        self.position = self.previous_position

