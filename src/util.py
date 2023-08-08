import pygame as pg

def get_middle(w: int, h: int, x: int, y: int) -> tuple[int, int]:
    return (x + w / 2, y + h / 2)

def get_middle_rect(rect: pg.Rect) -> tuple[int, int]:
    return get_middle(rect.w, rect.h, rect.x, rect.y)

def get_deltas_abs(x1: int, y1: int, x2: int, y2: int) -> tuple[int, int]:
    return (abs(x1 - x2), abs(y1 - y2))

def get_deltas(x1: int, y1: int, x2: int, y2: int) -> tuple[int, int]:
    return (x1 - x2, y1 - y2)

def get_top_left(w: int, h: int , x: int, y: int) -> tuple[int, int]:
    return (x - w / 2, y - h / 2)
