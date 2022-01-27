import sys

import pygame
from load_functions import load_image

clock = pygame.time.Clock()
fps = 60


def game_over(W, H, sc, file, win_par=()):
    pygame.mouse.set_visible(True)
    fon = pygame.transform.scale(load_image(file), (W, H))
    if win_par:
        font = pygame.font.Font(None, 100)
        enem = font.render(f"{win_par[0]}", True, (100, 255, 100))
        sc.blit(enem, (750, 280))

        diam = font.render(f"{win_par[1]}", True, (100, 255, 100))
        sc.blit(diam, (750, 385))
    sc.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(fps)


def terminate():
    pygame.quit()
    sys.exit()
