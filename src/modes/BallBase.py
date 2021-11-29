from core.cfg import SCR_SIZE
from core.core import *
from core.Colliders import *
from . import utils as ut
from .AudioManager import *
import copy
import random

class BallBase(Actor):
    def __init__(self, level: Level, pos: vec2, start_vel:int):
        super().__init__(level=level, size=vec2(1, 1), pos=pos)
        # cool down and particles
        self.ball_stopped = [True, True, 0, self.vel] #super list, that contains all you need for timer
        self.ball_stopped[3] = self.vel

        self.particle_system = None #for calling particles
        self.back_ground = None
        self.audio = Audio()
        
        # goals
        self.goal_can_happen = True
        self.players_goals = [0, 0]
        self.side = 1
        self.time_side = 1
        
        # initialization
        self.start_vel = start_vel
        self.collider = RectCollider(vec2(1, 1), pos)
        self.prev = self.collider
        self.reflections = 0

    def reflect(self):
        side = ut.sign(self.pos.y)
        vh = ut.sign(self.pos.y)  # vertical half

        # delta with border
        db = self.level.field.y * vh - \
            self.collider.top(-vh).y

        if ut.sign(db) == -vh:
            self.pos.y += 2 * db
            self.vel.y *= -1
            for i in range(5):
                self.particle_system.vertical_boom(side, 4)
            self.audio.play("boom")
                
    def check_goal(self):
        self.side = ut.sign(self.pos.x)
        if self.goal_can_happen and abs(self.pos.x) >= self.level.field.x:
            self.players_goals[-(self.side - 1) // 2] += 1
            for _ in range(10): #number of particles
                self.particle_system.horizontal_boom(self.side, 7)
            self.audio.play("goal_boom")
            self.time_side = self.side
            self.ball_stopped[0] = 1
            self.reflections = 0
            self.particle_system.trail_can_work = False
            self.back_ground.bg_brightness = 0

            self.goal_can_happen = False

        if not self.goal_can_happen and abs(self.pos.x) < self.level.field.x:
            self.goal_can_happen = True

    def timer(self, milisec, sd):
        if self.ball_stopped[0] and self.ball_stopped[1]:
            self.ball_stopped[2] = pg.time.get_ticks()
            self.pos = vec2(0, 0)
            self.vel = vec2(0, 0)
            self.ball_stopped[1] = False

        if not self.back_ground.win:
            if self.ball_stopped[0] and not self.ball_stopped[1]:
                if pg.time.get_ticks() - self.ball_stopped[2] > milisec:
                    self.particle_system.trail_can_work = True
                    a = (random.random() * 2 - 1)
                    self.vel = self.start_vel * vec2(math.cos(a), math.sin(a)) * sd
                    self.ball_stopped[0], self.ball_stopped[1]  = False, True

    def reset(self):
        if self.back_ground.win:
            key_pressed = pg.key.get_pressed()

            if key_pressed[pg.K_r]:
                self.back_ground.win = False
                self.players_goals[0],self.players_goals[1] = 0, 0

    def pre_phys(self, dt):
        self.prev = copy.copy(self.collider)
        return super().pre_phys(dt)

    def post_phys(self, dt):
        self.check_goal()
        self.reset()
        self.timer(1000, self.time_side)
        self.reflect()
        return super().post_phys(dt)

    def update(self, dt, upd_t=None) -> None:
        return super().update(dt, upd_t=upd_t)
