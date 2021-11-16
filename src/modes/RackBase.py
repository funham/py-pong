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

    def is_ball_behind(self):
        trace = SegCollider(self.ball.pos, self.ball.prev)
        print(f'{trace.p_list()=}')

        hit_surf = self.collider.left_seg(inv=self.side)
        print(f'{hit_surf.p_list()=}')
        # plt.plot([trace.p1.x, trace.p2.x],
        #          [trace.p1.y, trace.p2.y])
        # plt.plot([hit_surf.p1.x, hit_surf.p2.x],
        #          [hit_surf.p1.y, hit_surf.p2.y])

        # plt.show()
        if trace.inter_seg(hit_surf):
            print('hoba')
            #     return True

            # else:
            #     return False
        # pass

    def post_phys(self, dt):
        if self.is_ball_behind() and not self.coll:
            self.reflect_ball(dt)
            self.coll = True
        elif not self.is_ball_behind() and self.coll:
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
