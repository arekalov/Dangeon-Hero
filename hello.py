import sys

import pygame
from load_functions import load_image

clock = pygame.time.Clock()
fps = 60


def hello(W, H, sc, file):
    pygame.mouse.set_visible(True)
    fon = load_image(file)
    sc.blit(fon, (220, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return 'stop'
        pygame.display.flip()
        clock.tick(fps)


def terminate():
    pygame.quit()
    sys.exit()
