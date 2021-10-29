import pygame
from pygame import Vector2 as vec2, math
from pygame import display
from pygame import key
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, QUIT, K_w
from pygame.draw import rect
import math

RACK_DEFAULT_SIZE = vec2(5, 40)
RACK_VEL_MAX = 20


class Rack:
    def __init__(self, init_pos: vec2):
        self.rect = pygame.Rect(init_pos, RACK_DEFAULT_SIZE)
        self.sprite = pygame.transform.scale(
            pygame.image.load('../Assets/rack.png'), RACK_DEFAULT_SIZE)

    def move(self, keys, ws: vec2, dt: float):
        up = keys[K_UP] - keys[K_DOWN]
        #print(RACK_VEL_MAX * dt * up)
        self.rect.center -= vec2(0, RACK_VEL_MAX) * up * dt
