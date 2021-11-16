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

    def reflect_ball(self, dt):

        def cb(obj, sign) -> vec2: return obj.pos + sign * obj.size / 2

        rb = cb(self, -self.side).x
        bb = cb(self.ball, self.side).x

        dx = bb - rb

        self.ball.pos.x = self.ball.pos.x - 2 * dx
        self.ball.vel.x *= -1

    def collides_ball(self):
        trace = SegCollider(self.ball.pos, self.ball.prev)
        hit_surf = self.collider.left_seg(inv=self.side)

        return trace.inter_seg(hit_surf)

    def post_phys(self, dt):
        ball_hit = self.collides_ball()

        if ball_hit and not self.coll:
            self.reflect_ball(dt)
            self.coll = True
        elif not ball_hit and self.coll:
            self.coll = False

        self.constrain()

        return super().post_phys(dt)

    def update(self, dt, upd_t) -> None:
        super().update(dt, upd_t)


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
