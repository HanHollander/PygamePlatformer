import math
import pygame as pg
from pygame import Vector2

import collision
import graphics
import util
from physics import Position, c_GRAVITY
from elements import GroupElement, SpriteElement, CursorElement, PhysicsElement
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

        self.physics_objects = []
        self.physics_objects.append(
            PhysicsObject(
                pos=(100, 50),
                img=graphics.img_viking,
                physics_objects=self.physics_objects,
                max_velocity=1.0,
                mass=1,
                solid=True,
                gravity=True
            ))
        self.physics_objects.append(
            PhysicsObject(
                pos=(100, 100),
                img=platform,
                physics_objects=self.physics_objects,
                max_velocity=0.0,
                mass=1,
                solid=True,
                gravity=False
            ))

        for physics_object in self.physics_objects:
            world_group.add(physics_object.element)

    def update(self):
        self.background.update()
        self.cursor.update()
        for physics_object in self.physics_objects:
            physics_object.update()

    def on_mouse_motion(self, event: pg.event.Event):
        self.cursor.on_mouse_motion(event)

    def on_key_down(self, event: pg.event.Event):
        if event.key == pg.K_q:
            actions.quit()


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
        self.element.rect = pg.Rect(
            event.pos, (self.element.rect.w, self.element.rect.h))


class PhysicsObject:

    def __init__(self,
                 pos: tuple[int, int],
                 img: pg.Surface,
                 physics_objects: ["PhysicsObject"],
                 max_velocity: float,
                 mass: float,
                 solid: bool,
                 gravity: bool):
        self.element = PhysicsElement(pos, img)

        self.physics_objects = physics_objects

        self.position = Position(util.get_middle(self.element.image.get_width(),
                                                 self.element.image.get_height(),
                                                 pos[0],
                                                 pos[1]))  # (px, px)
        self.old_position = self.position
        self.force_vectors = [c_GRAVITY] if gravity else []
        self.max_velocity = max_velocity  # px/tick
        self.velocity = Vector2(0, 0)  # px/tick
        self.direction = 0  # rad
        self.mass = mass  # m
        self.solid = solid

    def update(self):
        self.element.old_rect = self.element.rect

        # apply collisions (update position)
        self.apply_force()

        # resolve collisions (update position again)
        collisions = self.get_collisions()
        self.resolve_collisions(collisions)

        new_rect = pg.Rect(util.get_top_left(self.element.image.get_width(),
                                             self.element.image.get_height(),
                                             self.position.x,
                                             self.position.y),
                           self.element.image.get_size())
        self.element.rect = new_rect

    def apply_force(self):
        # calculate force
        force_vector_sum = sum(self.force_vectors, Vector2())

        # apply force to velocity
        self.velocity.x = min(
            self.max_velocity, self.velocity.x + force_vector_sum.x / self.mass)
        self.velocity.y = min(
            self.max_velocity, self.velocity.y + force_vector_sum.y / self.mass)

        # apply velocity to position
        self.old_position = self.position
        self.position.xf = self.position.xf + self.velocity.x
        self.position.x = math.floor(self.position.xf)
        self.position.yf = self.position.yf + self.velocity.y
        self.position.y = math.floor(self.position.yf)

        # calculate direction
        dx = self.old_position.x - self.position.x
        dy = self.old_position.y - self.position.y
        self.direction = math.atan2(dy, dx)

    def get_collisions(self) -> dict["PhysicsObject", tuple[int, int]]:
        collisions = {}
        for i in range(0, len(self.physics_objects)):
            other = self.physics_objects[i]
            if other is not self and other.solid:
                overlap = pg.sprite.collide_mask(self.element, other.element);
                if overlap:
                    print("col", overlap)
                    collisions[other] = overlap
                else:
                    print("ncol")
                pass
        return collisions
    
    def resolve_collisions(self, collisions: dict["PhysicsObject", tuple[int, int]]):
        for collision in collisions:
            pass
            


