from core.Actor import Actor
from ..core.core import pg

class Bubble(Actor):
    def __init__(self, level: Level, sprite_path=None, size: vec2 = None, pos=..., vel=..., acc=...):
        super().__init__(level, sprite_path=sprite_path, size=size, pos=pos, vel=vel, acc=acc)