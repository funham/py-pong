# classic Pong

from .RackBase import *
from .BallBase import *


class RackClassic(RackBase):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float):
        super().__init__(level, pos, ball, max_vel)

    def pre_phys(self, dt):
        self.handle_input(dt, 2)

        return super().pre_phys(dt)


class RackClassicAI(RackBaseAI):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float, difficulty):
        super().__init__(level, pos, ball, max_vel, difficulty=difficulty)

    def pre_phys(self, dt):
        self.follow_ball(dt)
        return super().pre_phys(dt)


class BallClassic(BallBase):
    def __init__(self, level: Level, pos: vec2, vel=vec2(0, 0), start_vel=vec2(2, 0)):
        super().__init__(level, pos, vel=vel, start_vel=vec2(2, 0))
