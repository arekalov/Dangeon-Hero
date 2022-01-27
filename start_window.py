import sys

import pygame
from load_functions import load_image
from main import level_render

clock = pygame.time.Clock()
fps = 60
W = 1000
H = 510
sc = pygame.display.set_mode((W, H))


def peresech(x, y, tupl):
    return tupl[0] <= x <= tupl[2] and tupl[1] <= y <= tupl[3]


def start():
    fon = pygame.transform.scale(load_image('start.png'), (W, H))
    sc.blit(fon, (0, 0))
    buts = [(448, 187, 601, 242), (340, 291, 703, 394)]
    start = False
    map = ''
    while True:
        sc.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or start:
                if start:
                    callback = level_render(W, H, sc, map)
                    start = False
                    if callback != 'stop':
                        start = True
                        map = callback
                elif peresech(event.pos[0], event.pos[1], buts[0]):
                    callback = level_render(W, H, sc, 'learning.txt')
                    if callback != 'stop':
                        start = True
                        map = callback
                elif peresech(event.pos[0], event.pos[1], buts[1]):
                    callback = level_render(W, H, sc, 'level.txt')
                    if callback != 'stop':
                        start = True
                        map = callback
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    start()
