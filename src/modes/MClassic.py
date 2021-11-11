# classic Pong

from .RackBase import *
from .BallBase import *


class RackClassic(RackBase):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float):
        super().__init__(level, pos, ball, max_vel)

    def update(self, dt) -> None:
        # TODO add advanced reflections
        if self.rect.colliderect(self.ball.rect):
            self.ball.vel.x *= -1

        self.handle_input(self.max_vel)

        super().update(dt)
        super().check_bounds()


class RackClassicAI(RackBaseAI):
    def __init__(self, level: Level, pos: vec2, ball: BallBase, max_vel: float, difficulty):
        super().__init__(level, pos, ball, max_vel, difficulty=difficulty)

    def update(self, dt) -> None:
        super().follow_ball()
        super().update(dt)
        super().check_bounds()


class BallClassic(BallBase):
    def __init__(self, level: Level, pos: vec2, vel=vec2(0, 0)):
        super().__init__(level, pos, vel=vel)

    def update(self, dt) -> None:
        super().update(dt)
        super().reflect()
        super().check_goal()

