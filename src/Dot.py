import pygame
from pygame import Vector2 as vec2, math
from pygame import display
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, QUIT, K_w
from pygame.draw import rect
import math

DOT_VEL_MAX = 20


class Dot:
    def __init__(self, init_pos):
        self.rect = pygame.Rect(init_pos.x, init_pos.y, 5, 5)
        self.sprite = pygame.transform.scale(
            pygame.image.load('../Assets/dot.png'), (5, 5))

        self.vel = -vec2(DOT_VEL_MAX, DOT_VEL_MAX)

    def move(self, keys, ws: vec2, dt: float):

        if self.rect.top <= 0 and self.vel.y < 0:
            self.vel.y *= -1
            # self.rect.y = 0

        if self.rect.bottom >= ws.y and self.vel.y > 0:
            self.vel.y *= -1
            # self.rect.y = ws.y - self.rect.height

        if self.rect.left <= 0 and self.vel.x < 0:
            self.vel.x *= -1
            # self.rect.x = 0

        if self.rect.right >= ws.x and self.vel.x > 0:
            self.vel.x *= -1
            # self.rect.x = ws.x - self.rect.width

        self.rect.center += self.vel * dt
