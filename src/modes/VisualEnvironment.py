from pygame.constants import SCRAP_SELECTION
from core.core import *
from modes.BallBase import *


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

        pg.draw.line(self.scr, (0, 100, 0), (0, cfg.SCR_CENTER.y),
                     (cfg.SCR_SIZE.x, cfg.SCR_CENTER.y), 1)

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
