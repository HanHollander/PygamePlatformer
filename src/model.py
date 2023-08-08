from math import sqrt
import pygame as pg
import graphics
import util


import math


class PhysicsObject:
    def __init__(self, pos, max_velocity, velocity, direction, acceleration, mass):
        self.pos = util.Pos(pos)  # (px, px)
        self.max_velocity = max_velocity  # px/tick
        self.velocity = velocity  # px/tick
        self.direction = direction  # rad
        self.acceleration = acceleration  # px/tick²
        self.mass = mass  # -

    def update_pos(self) -> tuple[int, int]:
        vx = 
        # calculate new direction

        # correct direction (top left is 0,0)
        corrected_direction = -1 * self.direction

        # apply velocity
        self.pos.xf = self.pos.xf + self.velocity * math.cos(math.radians(corrected_direction))
        self.pos.yf = self.pos.yf + self.velocity * math.sin(math.radians(corrected_direction))
        self.pos.x = math.floor(self.pos.xf)
        self.pos.y = math.floor(self.pos.yf)
        return self.pos.x, self.pos.y

