from .BallBase import *
from .import utils as ut

import copy

# Base class for all Racket classes


class RackBase(Actor):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float):
        super().__init__(level=level,  # sprite_path='../Assets/rack.png',
                         size=vec2(1, 5), vel=vec2(0, 0), pos=pos)
        self.ball = ball
        self.max_vel = max_vel
        self.side = ut.sign(self.pos.x)
        self.coll = False

    # for some modes could be useful
    # should be added after apply_phys()
    def check_bounds(self):

        bounds = self.level.field

        # TODO cut the crap
        if self.pos.x - self.size.x / 2 <= -bounds.x:
            self.pos.x = -bounds.x + self.size.x / 2

        if self.pos.y - self.size.y / 2 <= -bounds.y:
            self.pos.y = -bounds.y + self.size.y / 2

        if self.pos.x + self.size.x / 2 >= bounds.x:
            self.pos.x = bounds.x - self.size.x / 2

        if self.pos.y + self.size.y / 2 >= bounds.y:
            self.pos.y = bounds.y - self.size.y / 2

    def reflect_ball(self, dt):

        def cb(obj, sign) -> vec2: return obj.pos + sign * obj.size / 2

        rb = cb(self, -self.side).x
        bb = cb(self.ball, self.side).x

        dx = bb - rb

        self.ball.pos.x = self.ball.pos.x - 2 * dx
        self.ball.vel.x *= -1

        # print(
        #     f'bb={bb}, rb={rb}, dx={dx}, s={-2*dx*self.side}')
        # print(f'next bb={ self.ball.pos.x + self.side * self.ball.size.x / 2}')

    def is_ball_behind(self):

        # calculate border function
        def cb(pos, size, sign) -> vec2: return pos + sign * size / 2

        in_y = cb(self.ball.np, self.ball.size, 1).y <= cb(self.pos, self.size, 1).y and \
            cb(self.ball.np, self.ball.size, -
               1).y >= cb(self.pos, self.size, -1).y

        in_x = self.ball.np.x * self.side >= self.pos.x * self.side

        # TODO check with correct trajectory
        return in_x and in_y

    # inherited sprite function
    # called automatically before drawing
    def update(self, dt) -> None:
        if self.is_ball_behind() and not self.coll:
            self.reflect_ball(dt)
            self.coll = True

        elif not self.is_ball_behind() and self.coll:
            self.coll = False

        super().apply_phys(dt)


# Base class for all Racket AI classes
class RackBaseAI(RackBase):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float, difficulty):
        super().__init__(level, pos, ball, max_vel)
        self.difficulty = difficulty

    def follow_ball(self):
        dy = (self.ball.pos - self.pos).y

        if dy > self.size.y / 2:
            self.vel.y = self.max_vel * ut.sign(dy)
        else:
            self.vel.y = min(self.max_vel, abs(self.ball.vel.y)) * ut.sign(dy)

    def update(self, dt) -> None:
        super().update(dt)  # applies physics as well
