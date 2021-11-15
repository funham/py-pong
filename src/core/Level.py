from . import cfg
from pygame import Vector2 as vec2
from Colliders import *


class Level:
    def __init__(self, field, origin=cfg.SCR_CENTER, scale=1.0):
        self.origin = origin
        self.scale = scale
        self.field = field
        self.collider = RectCollider(field * 2, vec2(0, 0))


lvl = Level(field=vec2(30, 15),
            origin=cfg.SCR_CENTER, scale=cfg.SCR_SIZE.y/30)
