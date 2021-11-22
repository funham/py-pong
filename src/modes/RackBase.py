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

        v = self.ball.vel.magnitude()
        v += 1 / self.ball.reflections
        a = height / self.size.y * math.pi / 2

        self.ball.vel = v * vec2(math.cos(a), math.sin(a))
        self.ball.vel.x *= -self.side
        
        self.ball.pos.x += delta.x * 0
        self.ball.reflections += 1

    def collides_ball(self):
        curr_bsurf = self.ball.collider.left_seg(inv=-self.side)
        prev_bsurf = self.ball.prev.left_seg(inv=self.side)

        # traces of top and bottom of ball surf
        top_trace = SegCollider(prev_bsurf.top(),
                                curr_bsurf.top())
        btm_trace = SegCollider(prev_bsurf.bottom(),
                                curr_bsurf.bottom())

        hit_surf = self.collider.left_seg(inv=self.side)

        inter_top = top_trace.inter_seg(hit_surf)
        inter_btm = btm_trace.inter_seg(hit_surf)

        if inter_top == None and inter_btm == None:
            return None

        if inter_top == None:
            return inter_btm

        if inter_btm == None:
            return inter_top

        return (inter_top + inter_btm) / 2

    def pre_phys(self, dt):
        ball_hit = self.collides_ball()
        if ball_hit and not self.coll:
            self.reflect_ball(ball_hit)
            self.coll = True
        elif not ball_hit and self.coll:
            self.coll = False

        return super().pre_phys(dt)

    def post_phys(self, dt):
        self.constrain()
        return super().post_phys(dt)

    def handle_input(self, dt):
        key_pressed = pygame.key.get_pressed()

        up = pygame.K_w if self.side < 0 else pygame.K_UP
        dn = pygame.K_s if self.side < 0 else pygame.K_DOWN

        dir = key_pressed[dn] - key_pressed[up]

        self.vel.y = ut.approach(
            self.vel.y, self.max_vel * dir, dt * self.max_vel)

# Base class for all Racket AI classes


class RackBaseAI(RackBase):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float, difficulty):
        super().__init__(level, pos, ball, max_vel)
        self.difficulty = difficulty

    def follow_ball(self, dt):
        dy = (self.ball.pos - self.pos).y

        t_vel = 0

        if abs(dy) > 2 / self.difficulty:
            if abs(dy) > self.size.y / 2:
                t_vel = self.max_vel * ut.sign(dy)
            else:
                t_vel = min(self.max_vel, abs(self.ball.vel.y)) * ut.sign(dy)

        t_vel *= self.difficulty
        self.vel.y = ut.approach(self.vel.y, t_vel, dt * self.max_vel)
