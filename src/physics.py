from enum import Enum
from pygame import Vector2
from util import pow_v2

class Position:
    def __init__(self, pos: tuple[int, int]):
        self.x = pos[0]
        self.y = pos[1]
        self.xf = self.x
        self.yf = self.y

    def __str__(self) -> str:
        return "[" + str(self.x) + ", " + str(self.y) + "]"

class Direction(Enum):
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)

    def absolute(self) -> Vector2:
        return pow_v2(self.value, 2)
    
    @staticmethod
    def get_direction(v: Vector2) -> "Direction":
        if v.x < 0:
            return Direction.LEFT
        elif v.y < 0:
            return Direction.UP
        elif v.x > 0:
            return Direction.RIGHT
        elif v.y > 0:
            return Direction.DOWN
        raise Exception(f"Should not happen: {v}")
        

c_GRAVITY = Vector2(0, 0.2)  # m px/tick²
c_AIR_DRAG_CONSTANT = 0.008
c_GROUND_DRAG_CONSTANT = 0.2
c_VELOCITY_CLIPPING_TRESHOLD_LOW = 0.15
c_VELOCITY_CLIPPING_TRESHOLD_HIGH = 999.9
c_FRICTION_COEFFICIENT = 1.1