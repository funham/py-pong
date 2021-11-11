from core.cfg import SCR_SIZE
from core.core import *


class BallBase(Actor):
    def __init__(self, level: Level, pos: vec2, vel=vec2(0, 0)):
        super().__init__(level=level,  # sprite_path='../Assets/ball.png',
                         size=vec2(1, 1), vel=vel, pos=pos)
        self.np = self.pos
        self.goal_can_happen = True
        self.players_goals = [0,0]

    def reflect(self):
        np = self.pos.y  # position
        ty = self.level.field.y  # y - threshold
        hh = self.size.y/2  # Half a Height

        # (+) & (-) bounds delta
        dt, db = ty - (np + hh), ty + (np - hh)

        if dt <= 0:
            self.vel.y *= -1
            self.pos.y += 2 * dt

        if db <= 0:
            self.vel.y *= -1
            self.pos.y -= 2 * db

    def check_goal(self):
        if self.goal_can_happen and self.pos.x <= -self.level.field.x:
            self.players_goals[1] += 1
            self.goal_can_happen = False

        if self.goal_can_happen and self.pos.x >= self.level.field.x:
            self.players_goals[0] += 1
            self.goal_can_happen = False

        if not self.goal_can_happen and self.pos.x > -self.level.field.x and self.pos.x < self.level.field.x:
            self.goal_can_happen = True

    def update(self, dt) -> None:
        super().apply_phys(dt)
        nv = self.vel + self.acc * dt
        self.np = self.pos + self.vel * dt
