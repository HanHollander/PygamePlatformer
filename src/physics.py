import math

class Position:
    def __init__(self, pos: tuple[int, int]):
        self.x = pos[0]
        self.y = pos[1]
        self.xf = self.x
        self.yf = self.y

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return "[" + str(self.x) + "," + str(self.y) + "]"

c_GRAVITY = Vector2(0, 9.81)  # kg px/tick²