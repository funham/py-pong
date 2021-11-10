import sys  # for sys.exit() at the end
from core.core import *
from modes.RackBase import *
from modes.MClassic import *
import core.Actor

import core.cfg as cfg
from modes.utils import sign

pg.init()
pg.display.set_caption('PongZ')
pg.display.set_icon(pg.image.load('../Assets/pong.png'))

scr = pg.display.set_mode(cfg.SCR_SIZE)
clock = pg.time.Clock()

ball_group = pg.sprite.Group()
ball = BallClassic(lvl, pos=vec2(0, 0), vel=vec2(1, 0.5))
ball_group.add(ball)

rack1 = RackClassicAI(level=lvl, pos=vec2(-lvl.field.x + 2, 0),
                      ball=ball, max_vel=20, difficulty=1)
rack2 = RackClassic(level=lvl, pos=vec2(lvl.field.x - 2, 0),
                      ball=ball, max_vel=5)

rack_group = pg.sprite.Group()

rack_group.add(rack1)
rack_group.add(rack2)

bg_brightness = cfg.BG_DEFAULT_BRIGHTNESS  # 0 - 255
rt = 0  # run time value

while True:

    # time passed since last frame
    dt = clock.tick(1000) / 100
    rt += dt

    # checking for events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # setting background color
    scr.fill(bg_brightness * pg.Vector3(1, 1, 1))

    # updating all sprite groups
    rack_group.update(dt)
    ball_group.update(dt)

    # drawing all sprite groups
    ball_group.draw(scr)
    rack_group.draw(scr)

    # putting image on the screen
    pg.display.update()
