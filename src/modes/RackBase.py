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
<<<<<<< HEAD
        angle = math.pi * height / self.size.y/2
        v = self.ball.vel.magnitude()
        self.ball.vel = v * vec2((-self.side) * math.cos(angle),
                                 math.sin(angle))
        self.ball.vel *= 1.05
=======
        v = self.ball.vel.magnitude()
        v += 0.5
        a = height / self.size.y * math.pi /2 

        self.ball.vel = v * vec2(math.cos(a), math.sin(a))
        self.ball.vel.x *= -self.side
>>>>>>> 349e729cad85da4e01f624229d0fb0cc900fdccb
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
        elif not ball_hit and self.coll:
            self.coll = False

        return super().pre_phys(dt)

    def post_phys(self, dt):
        self.constrain()
        return super().post_phys(dt)

    def handle_input(self, dt, acc):
        key_pressed = pygame.key.get_pressed()

        up_k = pygame.K_UP if self.side > 0 else pygame.K_w
        dn_k = pygame.K_DOWN if self.side > 0 else pygame.K_s

        # direction vector projection 
        dir = (key_pressed[dn_k] - key_pressed[up_k])

        # if nothing's pressed
        acc = 2 * dt
        if dir:
            # acc = dt * 2 if dir != ut.sign(self.vel.y) else 1
            
            self.vel.y = ut.approach(self.vel.y, dir * self.max_vel, acc)
        else:
            self.vel.y = ut.approach(self.vel.y, 0, acc)



# Base class for all Racket AI classes
class RackBaseAI(RackBase):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float, difficulty):
        super().__init__(level, pos, ball, max_vel)
        self.difficulty = difficulty

    def follow_ball(self):
        dy = (self.ball.pos - self.pos).y

        t_vel = 0

        if abs(dy) > 2 / self.difficulty:
            if abs(dy) > self.size.y / 2:
                t_vel = self.max_vel * ut.sign(dy)
            else:
                t_vel = min(self.max_vel, abs(self.ball.vel.y)) * ut.sign(dy)

        self.vel.y = t_vel

    def update(self, dt, upd_t) -> None:
        super().update(dt, upd_t)  # applies physics as well
