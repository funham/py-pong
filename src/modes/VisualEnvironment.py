import pygame as pg
from pygame.constants import BLEND_RGBA_ADD
from core.core import *
from modes.BallBase import *
import random


class BackGround(pg.sprite.Sprite):
    def __init__(self, scr, players_goals):
        super().__init__()
        self.scr = scr
        self.bg_brightness = cfg.BG_DEFAULT_BRIGHTNESS  # 0 - 255

        self.players_scores = players_goals
        self.font = pg.font.Font(None, 50)

    def draw_bg(self):
        pg.draw.rect(self.scr, pg.Color("white"),(cfg.SCR_SIZE.x/2-10, cfg.SCR_SIZE.y/2-10, 20, 20), 2)
        dot = 0

        for i in range(10):
            pg.draw.line(self.scr, pg.Color("white"), (cfg.SCR_SIZE.x / 2-1, dot), (cfg.SCR_SIZE.x/2-1, dot+10), 2)
            dot = dot + 20

        dot += 10

        for i in range(10):
            pg.draw.line(self.scr, pg.Color("white"), (cfg.SCR_SIZE.x / 2-1, dot), (cfg.SCR_SIZE.x/2-1, dot+10), 2)
            dot = dot + 20

    def draw_score(self):
        player1_score = self.font.render(str(self.players_scores[0]), False, pg.Color("white"))
        player2_score = self.font.render(str(self.players_scores[1]), False, pg.Color("white"))
        self.scr.blit(player1_score, (SCR_SIZE.x/2 -
                                      30 if self.players_scores[0] < 10 else SCR_SIZE.x/2 - 50, 20))
        self.scr.blit(player2_score, (SCR_SIZE.x/2+13, 20))

    def back_ground_filler(self):
        self.bg_brightness = ut.approach(self.bg_brightness, 30, 0.5)
        self.scr.fill(self.bg_brightness * pg.Vector3(1, 1, 1))

    def update(self):
        self.back_ground_filler()
        self.draw_bg()
        self.draw_score()

class ParticleSystem(pg.sprite.Sprite):

    class SingleParticle():
        def __init__(self, position, velocity, sizeQuotient, minusSizeQuotient = None):
            self.pos  = position
            self.vel  = velocity
            self.size = sizeQuotient
            self.minsize = minusSizeQuotient
  

    def __init__(self, scr, ball):
        self.scr  = scr

        self.ball = ball.rect
        self.particles = []
        self.trail_can_work = True

        pg.sprite.Sprite.__init__(self)


    def ball_trail(self, sizeQuotient, minusSizeQuotient = None): #pos, vel, radius
        pos  = vec2(self.ball.center)
        vel  = vec2(random.randint(-10, 10) / 10, random.randint(-10, 10) / 10)
        size = sizeQuotient
        minsize = minusSizeQuotient

        self.particles.append(self.SingleParticle(pos, vel, size, minsize))
        
        #=============================================================================
        #do not delete the following coments, because they may be useful in the future
        #=============================================================================
        #self.trails.append([[self.ball[0],self.ball[1]], [0,0], 13]) #pos, vell, transperency
        #for particle in self.particles:
        #    particle[0][0] += particle[1][0] #changing x
        #    particle[0][1] += particle[1][1] #changing y
        #    particle[2] -= 0.1                #changing transperency / length of trail
        #    s = pg.Surface((13,13))          #trail
        #    s.set_alpha(particle[2])
        #    s.fill((150,150,150))
        #    pg.transform.scale(s,(particle[2], particle[2]))
        #    self.scr.blit(s, (int(particle[0][0]), int(particle[0][1])), special_flags = BLEND_ADD)
        #    if particle[2] <= 0:
        #        self.particles.remove(particle) #removing transperence particles
        #=============================================================================

    def horizontal_boom(self, direction, sizeQuotient): 
        pos = vec2(self.ball.center)
        vel = vec2(-direction * random.randint(0, 20) / 10,
                                random.randint(-20, 20) / 10)
        size = random.randint(4, 8)*(sizeQuotient/10)

        self.particles.append(self.SingleParticle(pos, vel, size))

    def vertical_boom(self, direction, sizeQuotient):
        pos = vec2(self.ball.center)
        vel = vec2(             random.randint(-20, 20) / 10,
                   -direction * random.randint(0, 20) / 10)
        size = random.randint(4, 8)*(sizeQuotient/10)

        self.particles.append(self.SingleParticle(pos, vel, size))


    def circle_surf(self, radius, color):
        surf = pg.Surface((radius*2, radius*2))
        pg.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf

    def particle_updater(self):
        for particle in self.particles:
            particle.pos += particle.vel
            if particle.minsize: particle.size -= particle.minsize
            else: particle.size -= 0.1

            pg.draw.circle(self.scr, pg.Color("white"), particle.pos, particle.size)
            
            if particle.size <= 0:
                particle.size = 0
                self.particles.remove(particle)
            
            radius = particle.size * 2
            light_pos = vec2(particle.pos.x - radius, particle.pos.y - radius)
            self.scr.blit(self.circle_surf(radius, pg.Color("gray10")), light_pos, special_flags = BLEND_RGBA_ADD)
            radius = particle.size * 3
            light_pos = vec2(particle.pos.x - radius, particle.pos.y - radius)
            self.scr.blit(self.circle_surf(radius, pg.Color("gray10")), light_pos, special_flags = BLEND_RGBA_ADD)
            

    def update(self):
        if self.trail_can_work:
            self.ball_trail(3, 0.2) 
        self.particle_updater()

        

