from core.cfg import SCR_SIZE
from core.core import *
from core.Colliders import *
from . import utils as ut
import copy


class BallBase(Actor):
    def __init__(self, level: Level, pos: vec2, vel=vec2(0, 0), start_vel=None):
        super().__init__(level=level,  # sprite_path='../Assets/ball.png',
                         size=vec2(1, 1), vel=vel, pos=pos)
        self.goal_can_happen = True
        self.players_goals = [0, 0]

        self.start_vel = start_vel if start_vel else vec2(2, 0)
        self.collider = RectCollider(vec2(1, 1), pos)
        self.prev = self.pos

    def reflect(self):
        vh = ut.sign(self.pos.y)  # vertical half

        # delta with border
        db = self.level.field.y * vh - \
            self.collider.top(-vh).y

        if ut.sign(db) == -vh:
            self.pos.y += 2 * db
            self.vel.y *= -1

    def reset(self, side):
        self.pos = vec2(0, 0)
        self.vel = side * self.start_vel

    def check_goal(self):
        side = ut.sign(self.pos.x)
        if self.goal_can_happen and abs(self.pos.x) >= self.level.field.x:
            self.players_goals[(side + 1) // 2] += 1
            self.reset(side)
            self.goal_can_happen = False

        if not self.goal_can_happen and abs(self.pos.x) < self.level.field.x:
            self.goal_can_happen = True

    def pre_phys(self, dt):
        self.prev = copy.copy(self.pos)
        return super().pre_phys(dt)

    def post_phys(self, dt):
        self.check_goal()
        self.reflect()
        return super().post_phys(dt)

    def update(self, dt, upd_t=None) -> None:
        return super().update(dt, upd_t=upd_t)
