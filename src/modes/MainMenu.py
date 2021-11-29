
from .RackBase import *
from .BallBase import *


class Option(Actor):
    def __init__(self, level, name):
        super().__init__(level=level, size=(10, 5),
                         pos='''calculations''')
        self.name = name
        self.picked = False

    def light_up(self):
        pass


class RackMenu(RackBase):
    def __init__(self):
        pass

    def handle_input(self, dt):

        up = pygame.K_w if self.side < 0 else pygame.K_UP
        dn = pygame.K_s if self.side < 0 else pygame.K_DOWN

        dir = key_pressed[dn] - key_pressed[up]

        self.vel.y = ut.approach(
            self.vel.y, self.max_vel * dir, dt * self.max_vel)

    def pick_option(self):
        key_pressed = pygame.key.get_pressed()

        L = pygame.K_LEFT
        R = pygame.K_RIGHT

        dir = key_pressed[R] - key_pressed[L]


class BallMenu(BallBase):
    def __init__(self):
        pass
