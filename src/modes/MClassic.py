# classic Pong

from .RackBase import *
from .BallBase import *


class RackClassic(RackBase):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float):
        super().__init__(level, pos, ball, max_vel)

    def pre_phys(self, dt):
        self.handle_input(dt, self.max_vel)
        return super().pre_phys(dt)

    def post_phys(self, dt):
        return super().post_phys(dt)


class RackClassicAI(RackBaseAI):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float, difficulty):
        super().__init__(level, pos, ball, max_vel, difficulty=difficulty)

    def pre_phys(self, dt):
        self.follow_ball()
        return super().pre_phys(dt)


class BallClassic(BallBase):
    def __init__(self, level: Level, pos: vec2, vel=vec2(0, 0), rackets=None):
        super().__init__(level, pos, vel=vel)
