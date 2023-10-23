from pygame import Vector2

class Position:
    def __init__(self, pos: tuple[int, int]):
        self.x = pos[0]
        self.y = pos[1]
        self.xf = self.x
        self.yf = self.y

c_GRAVITY = Vector2(0, 9.81)  # m px/tick²