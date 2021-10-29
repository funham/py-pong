import pygame
from pygame import Vector2 as vec2, math
from pygame import display
from pygame.constants import K_DOWN, K_LEFT, K_RIGHT, K_UP, QUIT, K_w
import math

import matplotlib.pyplot as plt

from Dot import Dot
from Rack import *

FPS = 60

WIDTH, HEIGHT = 800, 600
WIN_SIZE = vec2(WIDTH, HEIGHT)
CENTER = vec2(WIDTH/2, HEIGHT/2)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


pygame.display.set_caption('the true PONG')


background = pygame.image.load('../Assets/background.png')
dot = Dot(CENTER)
rack1 = Rack(vec2(5, CENTER.y))


def draw_window(dot: Dot, rack: Rack):
    WINDOW.fill(pygame.Color(24, 24, 24))
    # WINDOW.blit(background, (0, 0))
    WINDOW.blit(dot.sprite, dot.rect)
    WINDOW.blit(rack.sprite, rack.rect)

    pygame.display.update()


def main_loop():
    fps_min = 100
    fps_max = 0
    rt = 0
    clock = pygame.time.Clock()
    run = True

    while run:
        dt = clock.tick(FPS) / 100  # returns dt in ms
        rt += dt  # run time (in seconds)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                print(fps_min, fps_max)

        keys_pressed = pygame.key.get_pressed()
        dot.move(keys_pressed, WIN_SIZE, dt)
        rack1.move(keys_pressed, WIN_SIZE, dt)

        # fps_min = min(fps_min, 1/dt)
        # fps_max = max(fps_max, 1/dt)
        draw_window(dot, rack1)

    pygame.quit()


if __name__ == '__main__':
    main_loop()
