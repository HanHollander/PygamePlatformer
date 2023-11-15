from enum import Enum
from pygame import Vector2

class Position:
    def __init__(self, pos: tuple[int, int]):
        self.x = pos[0]
        self.y = pos[1]
        self.xf = self.x
        self.yf = self.y

class Direction(Enum):
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)

    def absolute(self) -> Vector2:
        return self.value.elementwise() * self.value

c_GRAVITY = Vector2(0, 0.2)  # m px/tick²