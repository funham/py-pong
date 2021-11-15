from core.core import *
from core.Colliders import *
from . import utils as ut


class BallBase(Actor):
    def __init__(self, level: Level, pos: vec2, vel=vec2(0, 0), rackets=None):
        super().__init__(level=level,  # sprite_path='../Assets/ball.png',
                         size=vec2(1, 1), vel=vel, pos=pos)
        self.collider = RectCollider(vec2(1, 1), pos)
        self.prev = Actor(level=lvl, pos=pos, vel=vel,
                          collider=self.collider, size=self.size)

    def reflect(self):
        vh = ut.sign(self.pos.y)  # vertical half

        # delta with border
        db = self.level.field.y * vh - \
            self.collider.top(-vh).y

        if ut.sign(db) == -vh:
            self.pos.y += 2 * db
            self.vel.y *= -1

    def pre_phys(self, dt):
        self.prev.vel = self.vel
        self.prev.pre_phys(dt)

        return super().pre_phys(dt)

    def post_phys(self, dt):
        self.reflect()
        return super().post_phys(dt)
