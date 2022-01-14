import random

import pygame as pg
import sys

import pygame.display
from pygame.sprite import Sprite

W = 700
H = 500
sc = pg.display.set_mode((W, H))
clock = pygame.time.Clock()
fps = 60



cntrl = False
while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()


    pygame.display.flip()
    clock.tick(fps)
