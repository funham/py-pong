from math import nan
import pygame as pg
from pygame.time import Clock
from pygame.transform import scale
from core.cfg import SCR_CENTER
from core.core import *
from modes.BallBase import *
import random


class BackGround(pg.sprite.Sprite):
    def __init__(self, scr, players_goals):
        super().__init__()
        self.scr = scr
        self.players_scores = players_goals
        self.font = pg.font.Font(None, 50)

    def draw_bg(self):
        pg.draw.rect(self.scr, (250, 250, 250),
                     (cfg.SCR_SIZE.x/2-10, cfg.SCR_SIZE.y/2-10, 20, 20), 2)
        dot = 0

        for i in range(10):
            pg.draw.line(self.scr, (250, 250, 250), (cfg.SCR_SIZE.x /
                                                     2-1, dot), (cfg.SCR_SIZE.x/2-1, dot+10), 2)
            dot = dot + 20
        dot += 10

        for i in range(10):
            pg.draw.line(self.scr, (250, 250, 250), (cfg.SCR_SIZE.x /
                                                     2-1, dot), (cfg.SCR_SIZE.x/2-1, dot+10), 2)
            dot = dot + 20

    def draw_score(self):
        player1_score = self.font.render(
            str(self.players_scores[0]), False, (255, 255, 255))
        player2_score = self.font.render(
            str(self.players_scores[1]), False, (255, 255, 255))
        self.scr.blit(player1_score, (SCR_SIZE.x/2 -
                                      30 if self.players_scores[0] < 10 else SCR_SIZE.x/2 - 50, 20))
        self.scr.blit(player2_score, (SCR_SIZE.x/2+13, 20))

    def update(self):
        self.draw_bg()
        self.draw_score()

class ParticleSystem(pg.sprite.Sprite):

    def __init__(self, scr, ball):
        self.scr  = scr
        self.ball = ball.rect
        self.trails     = [] #list for trail behind ball
        self.booms = [] #list for goal explosions

        pg.sprite.Sprite.__init__(self)

    def ball_trail(self):
        currpos  = []
        currpos += [self.ball[0],self.ball[1]]
        
        self.trails.append([currpos, [0,0], 255]) #pos, vell, transperency
        
        for particle in self.trails:
            particle[0][0] += particle[1][0] #changing x
            particle[0][1] += particle[1][1] #changing y
            particle[2] -= 40                #changing transperency / length of trail
            s = pg.Surface((13,13))          #trail
            s.set_alpha(particle[2])
            s.fill((150,150,150))
            self.scr.blit(s, (int(particle[0][0]), int(particle[0][1])))
            if particle[2] <= 0:
                self.trails.remove(particle) #removing transperence particles

    def goal_boom(self, direction, size): 

        self.booms.append([[self.ball[0] + 3,self.ball[1]], [(-direction * random.randint(0, 20) / 10), random.randint(-20, 20) / 10]
                                    , random.randint(4, 8)*(size/10)]) #pos, vel, radius

    def wall_boom(self, direction, size):
        self.booms.append([[self.ball[0] + 3,self.ball[1]], [random.randint(-20, 20) / 10,-direction * random.randint(0, 20) / 10]
                                    , random.randint(4, 8)*(size/10)]) #pos, vel, radius

    def update(self):
        self.ball_trail()

        for boom in self.booms: # checking for goal
            boom[0][0] += boom[1][0] #changing x
            boom[0][1] += boom[1][1] #changing y
            boom[2] -= 0.1           #changing radius
            pg.draw.circle(self.scr, (255, 255, 255), [int(boom[0][0]), int(boom[0][1])], int(boom[2]))
            if boom[2] <= 0:
                self.booms.remove(boom) #removing very little particles

