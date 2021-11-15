from core.core import *
from core.Colliders import *


class BallBase(Actor):
    def __init__(self, level: Level, pos: vec2, vel=vec2(0, 0)):
        super().__init__(level=level,  # sprite_path='../Assets/ball.png',
                         size=vec2(1, 1), vel=vel, pos=pos, rackets=None)
        self.collider = RectCollider(vec2(1, 1), pos)

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

    def update(self, dt, upd_t) -> None:
        super().update(dt, upd_t=upd_t)
