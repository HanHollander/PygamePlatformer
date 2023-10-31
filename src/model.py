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
from view import View


class Game:

    def __init__(self, view: View):
        self.cursor = Cursor()
        view.add(self.cursor.element)

        platform = pg.Surface(
            size=(150, 10)
        )
        platform.fill((255, 255, 255))

        self.physics_objects = []
        self.physics_objects.append(
            Player(
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
            view.add(physics_object.element)

    def update(self):
        self.cursor.update()
        for physics_object in self.physics_objects:
            physics_object.update()

    def on_mouse_motion(self, event: pg.event.Event):
        self.cursor.on_mouse_motion(event)

    def on_key_down(self, event: pg.event.Event):
        if event.key == pg.K_q:
            actions.quit()
        for physics_object in self.physics_objects:
            if isinstance(physics_object, Player):
                physics_object.on_key_down(event)


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
        self.const_forces = [c_GRAVITY] if gravity else []
        self.temp_forces = []
        self.max_velocity = max_velocity  # px/tick
        self.velocity = Vector2(0, 0)  # px/tick
        self.mass = mass  # m
        self.solid = solid

    def update(self):
        # apply collisions (update position)
        self.apply_force()

        self.sync_element()

        # resolve collisions (update position again)
        # collisions = self.get_collisions()
        # self.resolve_collisions(collisions)
        self.resolve_collisions_simple()

        self.temp_forces.clear()

    def sync_element(self):
        self.element.rect = pg.Rect(util.get_top_left(self.element.image.get_width(),
                                                      self.element.image.get_height(),
                                                      self.position.x,
                                                      self.position.y),
                                    self.element.image.get_size())

    def apply_force(self):
        # calculate force
        force_vector_sum = sum(self.const_forces, Vector2())
        force_vector_sum = sum(self.temp_forces, force_vector_sum)

        # check if standing
        if self.is_standing():
            force_vector_sum -= c_GRAVITY

        # apply force to velocity
        self.velocity.x = min(
            self.max_velocity, self.velocity.x + force_vector_sum.x / self.mass)
        self.velocity.y = min(
            self.max_velocity, self.velocity.y + force_vector_sum.y / self.mass)

        # apply velocity to position
        self.position.xf = self.position.xf + self.velocity.x
        self.position.x = math.floor(self.position.xf)
        self.position.yf = self.position.yf + self.velocity.y
        self.position.y = math.floor(self.position.yf)

    def get_collisions(self) -> dict["PhysicsObject", tuple[int, int]]:
        collisions = {}
        for i in range(0, len(self.physics_objects)):
            other = self.physics_objects[i]
            if other is not self and other.solid:
                overlap = pg.sprite.collide_mask(self.element, other.element)
                if overlap:
                    print("col", overlap)
                    collisions[other] = overlap
                else:
                    print("ncol")
        return collisions

    def is_colliding(self) -> bool:
        for i in range(0, len(self.physics_objects)):
            other = self.physics_objects[i]
            if other is not self and other.solid:
                overlap = pg.sprite.collide_mask(self.element, other.element)
                if overlap:
                    return True
        return False
    
    def is_standing(self) -> bool:
        for i in range(0, len(self.physics_objects)):
            other = self.physics_objects[i]
            if other is not self and other.solid:
                overlap = self.element.mask.overlap(other.element.mask, 
                                          (other.element.rect.x - self.element.rect.x, 
                                           other.element.rect.y - self.element.rect.y - 1))
                if overlap:
                    return True
        return False

    def resolve_collisions(self, collisions: dict["PhysicsObject", tuple[int, int]]):
        pass

    def resolve_collisions_simple(self):
        if self.velocity.x != 0 or self.velocity.y != 0:
            l = math.sqrt(math.pow(self.velocity.x, 2) +
                        math.pow(self.velocity.y, 2))
            dx = -1 * self.velocity.x / l
            dy = -1 * self.velocity.y / l
            while self.is_colliding():
                self.position.xf = self.position.xf + dx
                self.position.x = math.floor(self.position.xf)
                self.position.yf = self.position.yf + dy
                self.position.y = math.floor(self.position.yf)
                self.sync_element()

class Player(PhysicsObject):

    def __init__(self, 
                 pos: tuple[int, int], 
                 img: pg.Surface, 
                 physics_objects: ["PhysicsObject"], 
                 max_velocity: float, 
                 mass: float, 
                 solid: bool, 
                 gravity: bool):
        PhysicsObject.__init__(self,
                               pos, 
                               img, 
                               physics_objects, 
                               max_velocity, 
                               mass, 
                               solid, 
                               gravity)
        
    def on_key_down(self, event: pg.event.Event):
        if event.key == pg.K_UP:
            self.temp_forces.append(-1.5 * c_GRAVITY)