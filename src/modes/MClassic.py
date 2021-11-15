# classic Pong

from .RackBase import *
from .BallBase import *


class RackClassic(RackBase):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float):
        super().__init__(level, pos, ball, max_vel)

    def pre_phys(self, dt):
        return super().pre_phys(dt)

    def post_phys(self):
        if self.rect.colliderect(self.ball.rect):
            self.ball.vel.x *= -1

        return super().post_phys()

    def update(self, dt, upd_t) -> None:

        # TODO add advanced reflections

        super().update(dt, upd_t)
        super().constrain(dt)


class RackClassicAI(RackBaseAI):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float, difficulty):
        super().__init__(level, pos, ball, max_vel, difficulty=difficulty)

    def update(self, dt, upd_t=None) -> None:
        super().follow_ball()
        super().update(dt, upd_t)


class BallClassic(BallBase):
    def __init__(self, level: Level, pos: vec2, vel=vec2(0, 0), rackets=None):
        super().__init__(level, pos, vel=vel)

    def update(self, dt, upd_t=None) -> None:
        super().update(dt, upd_t=upd_t)
        super().reflect()
