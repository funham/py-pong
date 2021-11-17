import pygame
from pygame import key
from .BallBase import *
from .import utils as ut
import matplotlib.pyplot as plt

import copy

# Base class for all Racket classes


class RackBase(Actor):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float):
        super().__init__(level=level,  # sprite_path='../Assets/rack.png',
                         size=vec2(1, 5), vel=vec2(0, 0), pos=pos,
                         collider=RectCollider(size=vec2(1, 5), pos=pos))
        self.ball = ball
        self.max_vel = max_vel
        self.side = ut.sign(self.pos.x)
        self.coll = False
        self.c = 0

    # for some modes could be useful
    # should be added after apply_phys()
    def constrain(self):
        bounds = self.level.field

        if self.pos.y - self.size.y / 2 <= -bounds.y:
            self.pos.y = -bounds.y + self.size.y / 2
            self.vel.y = 0

        if self.pos.y + self.size.y / 2 >= bounds.y:
            self.pos.y = bounds.y - self.size.y / 2
            self.vel.y = 0

    def reflect_ball(self, int_p):
        '''
        takes the point ball hit racket in (intersection point)
        '''
        # delta with current ball position and hit point
        delta = vec2(self.ball.pos - int_p)
        height = (int_p - self.pos).y  # will define reflected angle... someday
        self.ball.vel.x *= -1
        self.ball.pos.x += delta.x * 0

    def collides_ball(self):
        ball_surf = self.ball.collider.left(inv=-self.side)
        trace = SegCollider(self.ball.prev, ball_surf)
        hit_surf = self.collider.left_seg(inv=self.side)

        return trace.inter_seg(hit_surf)

    def pre_phys(self, dt):
        ball_hit = self.collides_ball()
        if ball_hit and not self.coll:
            self.reflect_ball(ball_hit)
            self.coll = True
            print(self.c)
            self.c += 1
        elif not ball_hit and self.coll:
            self.coll = False

        return super().pre_phys(dt)

    def post_phys(self, dt):
        self.constrain()
        return super().post_phys(dt)

    def handle_input(self, vel):
        key_pressed = pygame.key.get_pressed()

        # difference between Up and Down
        UpDown_diff = (key_pressed[pygame.K_DOWN] - key_pressed[pygame.K_UP])
        # difference between W and S
        WS_diff = (key_pressed[pygame.K_s] - key_pressed[pygame.K_w])

        if self.side > 0:
            self.vel.y = vel * UpDown_diff  # left racket
        if self.side < 0:
            self.vel.y = vel * WS_diff  # right racket


# Base class for all Racket AI classes
class RackBaseAI(RackBase):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float, difficulty):
        super().__init__(level, pos, ball, max_vel)
        self.difficulty = difficulty

    def follow_ball(self):
        dy = (self.ball.pos - self.pos).y

        t_vel = 0

        if abs(dy) > self.size.y / 2:
            t_vel = self.max_vel * ut.sign(dy)
        else:
            t_vel = min(self.max_vel, abs(self.ball.vel.y)) * ut.sign(dy)

        self.vel.y = t_vel

    def update(self, dt, upd_t) -> None:
        super().update(dt, upd_t)  # applies physics as well
