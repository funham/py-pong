from pygame.transform import scale
from . import cfg
from pygame import Vector2 as vec2
from .Colliders import *


class Level:
    def __init__(self, field, origin=cfg.SCR_CENTER, scale=1.0):
        self.origin = origin
        self.scale = scale
        self.field = field

        self.collider = RectCollider(field * 2, vec2(0, 0))
    
    def pos2pixel(self, pos : vec2) -> vec2:
        '''takes position in relative coords and returns pixel on screen'''
        return self.origin + pos / self.scale

    def pixel2pos(self, pixel : vec2) -> vec2:
        '''takes pixel on screen and returns position in relative coords'''
        return (pixel - self.origin) * self.scale



lvl = Level(field=vec2(30, 15), origin=cfg.SCR_CENTER, scale=cfg.SCR_SIZE.y/30)