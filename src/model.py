from math import sqrt
import pygame as pg
import graphics
import util
import physics


import math


class PhysicsObject:
    def __init__(self, pos, max_velocity, direction, mass):
        self.position = physics.Position(pos)  # (px, px)
        self.force_vectors = [physics.c_GRAVITY]
        self.max_velocity = max_velocity  # px/tick
        self.velocity = physics.Vector2(0, 0)  # px/tick
        self.direction = direction  # rad
        self.mass = mass  # kg

    def update_pos(self) -> tuple[int, int]:
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
        return self.position.x, self.position.y

