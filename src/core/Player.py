from .core import pg
from ..main import *

class Player:
    '''
    Contains information about players.
    '''
    def __init__(self, rack1: RackClassic, rack2: RackClassic, ball: BallClassic):
        self.rack1 = rack1
        self.rack2 = rack2
        self.ball  = ball
        self.first_player_score  = ball.players_goals[0]
        self.second_player_score = ball.players_goals[1]