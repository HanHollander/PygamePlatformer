from math import sqrt
import pygame as pg
import graphics
import util


import math


class PhysicsObject:
    def __init__(self) -> None:
        self.max_velocity = 0  # px/s
        self.velocity = 0  # px/s
        self.direction = 0  # rad

