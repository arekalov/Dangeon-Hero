import sys

import pygame
from load_functions import load_image

clock = pygame.time.Clock()
fps = 60


def peresech(x, y, tupl):
    return tupl[0] <= x <= tupl[2] and tupl[1] <= y <= tupl[3]


def pause(W, H, sc):
    fon = pygame.transform.scale(load_image('pause.png'), (W, H))
    sc.blit(fon, (0, 0))
    buts = [(360, 185, 718, 235), (360, 255, 718, 305), (360, 325, 718, 375)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return  # начинаем игру
            if event.type == pygame.MOUSEBUTTONDOWN:
                if peresech(event.pos[0], event.pos[1], buts[0]):
                    return 'menu'
                elif peresech(event.pos[0], event.pos[1], buts[1]):
                    return
                elif peresech(event.pos[0], event.pos[1], buts[2]):
                    return 'restart'
        pygame.display.flip()
        clock.tick(fps)


def terminate():
    pygame.quit()
    sys.exit()
