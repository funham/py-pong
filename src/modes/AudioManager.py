import pygame as pg
from core.core import *
from modes.BallBase import *
import random

class Audio(pg.mixer.Sound):
    def __init__(self):
        self.boom = pg.mixer.Sound("../Assets/Sounds/Hit.wav")
        self.goal_boom1 = pg.mixer.Sound("../Assets/Sounds/Explosion1.wav")
        self.goal_boom2 = pg.mixer.Sound("../Assets/Sounds/Explosion2.wav")
        self.goal_boom3 = pg.mixer.Sound("../Assets/Sounds/Explosion3.wav")
        #self.main_theme = pg.mixer.music.load("../Assets/Sounds/MainTheme.mp3")
        #self.game_over  = pg.mixer.Sound("../Assets/Sounds/GameOver.mp3  ")
        
    def play(self, audio_path = None):
        if audio_path == "boom":
            self.boom.play()
            
        if audio_path == "goal_boom":
            rand = random.randint(1,3)
            if   rand == 1: self.goal_boom1.play()
            elif rand == 2: self.goal_boom2.play()
            elif rand == 3: self.goal_boom3.play()
