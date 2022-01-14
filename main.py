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

hero_group = pygame.sprite.Group()


class Hero(pygame.sprite.Sprite):
    image = pygame.image.load("data\\characters_sprites\\hero-1.png")

    def __init__(self):
        super(Hero, self).__init__(hero_group)
        self.image = Hero.image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10



cntrl = False
hero = Hero()
while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            hero.rect.x += 10
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            hero.rect.x -= 10
        if pygame.key.get_pressed()[pygame.K_UP]:
            hero.rect.y -= 10
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            hero.rect.y += 10
    pygame.display.flip()
    sc.fill((0, 0, 0))
    hero_group.draw(sc)
    clock.tick(fps)
