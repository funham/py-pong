# classic Pong

from .RackBase import *
from .BallBase import *


class RackClassic(RackBase):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float):
        super().__init__(level, pos, ball, max_vel)

    def pre_phys(self, dt):
        self.handle_input(dt)

        return super().pre_phys(dt)


class RackClassicAI(RackBaseAI):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float):
        super().__init__(level, pos, ball, max_vel)

    def pre_phys(self, dt):
        self.follow_ball(dt)
        return super().pre_phys(dt)


class BallClassic(BallBase):
    def __init__(self, level: Level, pos: vec2, start_vel):
        super().__init__(level=level, pos=pos, start_vel=start_vel)
