from .core import pg
from .core import vec2
from .Level import *


class Actor(pg.sprite.Sprite):
    def __init__(self, level: Level, sprite_path=None, size: vec2 = None, pos=vec2(0, 0),
                 vel=vec2(0, 0), acc=vec2(0, 0), collider=None) -> None:
        super().__init__()
        self.level = level
        self.size = size

        if sprite_path:
            self.image = pg.image.load(sprite_path)
        else:
            self.image = pg.surface.Surface(size)
            self.image.fill('#ffffff')

        self.rect = self.image.get_rect()
        if size:
            self.rect.size = size

        self.rect.center = pos
        self.vel = vel
        self.pos = pos
        self.acc = acc

        if collider:
            self.collider = collider

    def apply_phys(self, dt):
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        self.rect.center = self.pos * self.level.scale + self.level.origin
        self.rect.size = self.size * self.level.scale
        self.image = pg.transform.scale(
            self.image, self.size * self.level.scale)

    def update(self, dt) -> None:
        return super().update()
