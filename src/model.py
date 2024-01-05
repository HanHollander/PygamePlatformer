import math
import pygame as pg
from pygame import Vector2

import collision
import graphics
import util
import physics as ps
from elements import GroupElement, SpriteElement, CursorElement, PhysicsElement
import config
import actions
import debug
from view import GUIView, View


class Game:

    def __init__(self, view: View):
        self.keys_down: set[int] = set()

        platform = pg.Surface(
            size=(300, 10)
        )
        platform.fill((255, 255, 255))

        wall = pg.Surface(
            size=(10, 100)
        )
        wall.fill((118, 29, 181))

        self.physics_objects = []
        self.physics_objects.append(
            Player(
                pos=(100, 50),
                img=graphics.img_viking,
                game=self,
                max_velocity=1.0,
                mass=1,
                solid=True,
                gravity=True
            ))
        self.physics_objects.append(
            PhysicsObject(
                pos=(10, 170),
                img=platform,
                game=self,
                max_velocity=0.0,
                mass=1,
                solid=True,
                gravity=False
            ))
        self.physics_objects.append(
            PhysicsObject(
                pos=(10, 60),
                img=wall,
                game=self,
                max_velocity=0.0,
                mass=1,
                solid=True,
                gravity=False
            ))

        for physics_object in self.physics_objects:
            view.add(physics_object.element)

            # Center on the player
            if isinstance(physics_object, Player):
                view.center_element = physics_object.element

    def update(self):
        for physics_object in self.physics_objects:
            physics_object.update()

    def on_key_down(self, event: pg.event.Event):
        self.keys_down.add(event.key)
        if event.key == pg.K_q:
            actions.quit()
        for physics_object in self.physics_objects:
            if isinstance(physics_object, Player):
                physics_object.on_key_down(event)
    
    def on_key_up(self, event: pg.event.Event):
        self.keys_down.remove(event.key)
        for physics_object in self.physics_objects:
            if isinstance(physics_object, Player):
                physics_object.on_key_up(event)


class UILayer:

    def __init__(self, view: GUIView) -> None:
        self.cursor = Cursor()
        view.add(self.cursor.element)

    def on_mouse_motion(self, event: pg.event.Event):
        self.cursor.on_mouse_motion(event)


class Cursor:
    def __init__(self):
        self.element = CursorElement(
            pos=(20, 240 - graphics.img_cursor.get_size()[1] / 2),
            img=graphics.img_cursor
        )

    def on_mouse_motion(self, event: pg.event.Event):
        self.element.rect = pg.Rect(
            event.pos, (self.element.rect.w, self.element.rect.h))


class PhysicsObject:

    def __init__(self,
                 pos: tuple[int, int],
                 img: pg.Surface,
                 game: "Game",
                 max_velocity: float,
                 mass: float,
                 solid: bool,
                 gravity: bool):
        self.element = PhysicsElement(pos, img)

        self.game = game

        self.position = ps.Position(util.get_middle(self.element.image.get_width(),
                                                 self.element.image.get_height(),
                                                 pos[0],
                                                 pos[1]))  # (px, px)
        self.const_forces = [ps.c_GRAVITY * mass] if gravity else []
        self.temp_forces = []
        self.max_velocity = max_velocity  # px/tick
        self.velocity = Vector2(0, 0)  # px/tick
        self.mass = mass  # m
        self.solid = solid

    def update(self):
        # apply collisions (update position)
        self.apply_force()

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
        # add reaction forces and limit velocity
        reaction_forces: list[Vector2] = []
        for direction in ps.Direction:
            if self.is_touching(direction):
                for force in (self.const_forces + self.temp_forces):
                    if force * direction.value > 0:
                        reaction_forces.append(force.elementwise() * (direction.absolute()) * -1)
                if self.velocity * direction.value > 0:
                    # BOUNCE 2*
                    self.velocity = self.velocity - (self.velocity.elementwise() * direction.absolute())

        # clip velocity
        if util.mag_v2(self.velocity) < ps.c_VELOCITY_CLIPPING_TRESHOLD_LOW:
            self.velocity = Vector2(0, 0)
        # elif util.mag_v2(self.velocity) > c_VELOCITY_CLIPPING_TRESHOLD_HIGH:
        #     self.velocity = Vector2(c_VELOCITY_CLIPPING_TRESHOLD_HIGH, c_VELOCITY_CLIPPING_TRESHOLD_HIGH)
        
        # add drag F_D = C_D * A * rho * V² / 2
        # F_D = drag force
        # A = reference area
        # rho is fluid density
        # V = flow velocity
        # simplified: F_D = K * V² where K = C_D * A * rho / 2
        drag_forces: list[Vector2] = []
        # air drag
        # TODO maybe magnitude squared then split into vector idk?
        drag_forces.append(-1 * ps.c_AIR_DRAG_CONSTANT * util.spow_v2(self.velocity, 2))

        # add dry friction F_f = mu * N
        # F_f = friction force opposed to velocity direction
        # mu = friction coefficient (constant dimensionless)
        # N = normal force
        friction_forces: list[Vector2] = []
        # static/kinetic friction
        for reaction_force in reaction_forces:
            normal_direction = ps.Direction.get_direction(reaction_force)
            if normal_direction in (ps.Direction.UP, ps.Direction.DOWN) and self.velocity.x != 0:
                friction_direction = ps.Direction.RIGHT if self.velocity.x < 0 else ps.Direction.LEFT
                friction_forces.append(ps.c_FRICTION_COEFFICIENT * abs(reaction_force.y) * friction_direction.value)
            elif normal_direction in (ps.Direction.LEFT, ps.Direction.RIGHT) and self.velocity.y != 0:
                friction_direction = ps.Direction.DOWN if self.velocity.y < 0 else ps.Direction.UP
                friction_forces.append(ps.c_FRICTION_COEFFICIENT * abs(reaction_force.x) * friction_direction.value)

        # calculate force
        force_vector_sum = sum(self.const_forces, Vector2())
        force_vector_sum = sum(self.temp_forces, force_vector_sum)
        force_vector_sum = sum(reaction_forces, force_vector_sum)
        force_vector_sum = sum(drag_forces, force_vector_sum)
        force_vector_sum = sum(friction_forces, force_vector_sum)
        if config.DEBUG_INFO and isinstance(self, Player): debug.debug["force vector sum"] = force_vector_sum

        # apply force to velocity
        self.velocity.x = self.velocity.x + force_vector_sum.x / self.mass
        self.velocity.y = self.velocity.y + force_vector_sum.y / self.mass

        # apply velocity to position
        self.position.xf = self.position.xf + self.velocity.x
        self.position.x = math.floor(self.position.xf)
        self.position.yf = self.position.yf + self.velocity.y
        self.position.y = math.floor(self.position.yf)
        self.sync_element()

    def get_collisions(self) -> dict["PhysicsObject", tuple[int, int]]:
        collisions = {}
        for i in range(0, len(self.game.physics_objects)):
            other = self.game.physics_objects[i]
            if other is not self and other.solid:
                overlap = pg.sprite.collide_mask(self.element, other.element)
                if overlap:
                    print("col", overlap)
                    collisions[other] = overlap
                else:
                    print("ncol")
        return collisions

    def is_colliding(self) -> bool:
        for i in range(0, len(self.game.physics_objects)):
            other = self.game.physics_objects[i]
            if other is not self and other.solid:
                overlap = pg.sprite.collide_mask(self.element, other.element)
                if overlap:
                    return True
        return False
    
    def is_touching(self, direction: ps.Direction) -> None:
        for i in range(0, len(self.game.physics_objects)):
            other = self.game.physics_objects[i]
            if other is not self and other.solid:
                overlap = self.element.mask.overlap(other.element.mask,
                                          (other.element.rect.x - self.element.rect.x - direction.value.x,
                                           other.element.rect.y - self.element.rect.y - direction.value.y))
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
                 game: "Game",
                 max_velocity: float, 
                 mass: float, 
                 solid: bool, 
                 gravity: bool):
        PhysicsObject.__init__(self,
                               pos, 
                               img, 
                               game, 
                               max_velocity, 
                               mass, 
                               solid, 
                               gravity)
        
    def update(self):
        self.add_player_input_forces()
        PhysicsObject.update(self)
        if config.DEBUG_INFO: 
            debug.debug["velocity"] = self.velocity
            debug.debug["position"] = self.position

    def add_player_input_forces(self):
        for key in self.game.keys_down:
            if key == pg.K_UP and self.is_touching(ps.Direction.DOWN):
                self.temp_forces.append(-50 *ps.c_GRAVITY)
            elif key == pg.K_LEFT:
                self.temp_forces.append(Vector2(-0.4, 0))
            elif key == pg.K_RIGHT:
                self.temp_forces.append(Vector2(0.4, 0))
        
    def on_key_down(self, event: pg.event.Event):
        pass

    def on_key_up(self, event: pg.event.Event):
        pass