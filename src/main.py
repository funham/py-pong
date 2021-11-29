import sys  # for sys.exit() at the end

from core.core import *
from modes.RackBase import *
from modes.MClassic import *
from modes.VisualEnvironment import *

import core.cfg as cfg
from modes.utils import sign

pg.init()

pg.display.set_caption('PongZ')
pg.display.set_icon(pg.image.load('../Assets/pong.png'))

scr = pg.display.set_mode(cfg.SCR_SIZE)
clock = pg.time.Clock()


ball_group = pg.sprite.Group()
rack_group = pg.sprite.Group()

ball = BallClassic(lvl, pos=vec2(0, 0), start_vel=2)
ball_group.add(ball)

rack1 = RackClassicAI(level=lvl, pos=vec2(lvl.field.x - 2, 0),
                    ball=ball, max_vel=5)
rack2 = RackClassicAI(level=lvl, pos=vec2(-lvl.field.x + 2, 0),
                      ball=ball, max_vel=5)

ball.racks = [rack1, rack2]

rack_group.add(rack1)
rack_group.add(rack2)

visual_group = pg.sprite.Group()

background = BackGround(scr, ball.players_goals)
particle_sys = ParticleSystem(scr, ball)

ball.particle_system = particle_sys
ball.back_ground = background

visual_group.add(background)
visual_group.add(particle_sys)

rt = 0  # run time value

while True:

    # time passed since last frame
    dt = clock.tick(60) / 100
    rt += dt

    # checking for events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()


    # updating all sprite groups
    visual_group.update()
    rack_group.update(dt, UPD.PRE)
    ball_group.update(dt, UPD.PRE)
    

    ball_group.update(dt, UPD.POST)
    rack_group.update(dt, UPD.POST)

    # drawing all sprite groups
    ball_group.draw(scr)
    rack_group.draw(scr)
    
    # putting image on the screen
    pg.display.update()
