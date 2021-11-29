from core.cfg import SCR_SIZE
from core.core import *
from core.Colliders import *
from . import utils as ut
import copy


class BallBase(Actor):
    def __init__(self, level: Level, pos: vec2, start_vel):
        super().__init__(level=level, size=vec2(1, 1), pos=pos, vel=start_vel)
        # cool down and particles
        self.ball_stopped = [False, True, 0, self.vel] #super list, that contains all you need for timer
        self.ball_stopped[3] = self.vel
        self.particle_system = None #for calling particles
        self.back_ground = None
        
        # goals
        self.goal_can_happen = True
        self.players_goals = [0, 0]
        
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
                
    def check_goal(self):
        self.side = ut.sign(self.pos.x)
        if self.goal_can_happen and abs(self.pos.x) >= self.level.field.x:
            self.players_goals[-(self.side - 1) // 2] += 1
            for _ in range(10): #number of particles
                self.particle_system.horizontal_boom(self.side, 7)
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
            self.vel = vec2(0,0)
            self.ball_stopped[1] = False

        if self.ball_stopped[0] and not self.ball_stopped[1]:
            if pg.time.get_ticks() - self.ball_stopped[2] > milisec:
                self.vel = sd * self.start_vel
                self.particle_system.trail_can_work = True
                self.ball_stopped[0], self.ball_stopped[1]  = False, True

    def pre_phys(self, dt):
        self.prev = copy.copy(self.collider)
        return super().pre_phys(dt)

    def post_phys(self, dt):
        self.check_goal()
        self.timer(1000, self.side)
        self.reflect()
        return super().post_phys(dt)

    def update(self, dt, upd_t=None) -> None:
        return super().update(dt, upd_t=upd_t)
