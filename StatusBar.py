import pygame
from load_functions import load_image


class StatusBar:  # Класс счетчика жизней, убийств, алмазов
    def __init__(self, hp, sc):
        self.hp = hp
        self.sc = sc  # Screen для работы
        self.enemies = 0
        self.diamonds = 0
        self.draw()

    def draw(self):  # Функция отрисовки счетчика
        font = pygame.font.Font(None, 20)
        text = font.render(f"       x{self.diamonds}         x{self.hp}          x{self.enemies}", True,
                           (100, 255, 100))  # Создание надписи
        self.sc.blit(text, (0, 10))  # Hазмещение надписи
        diam = load_image('diamond.png')  # Подгрузка изображений
        heart = load_image('heart.png')
        enemy = load_image('enemy_killed.png')
        self.sc.blit(enemy, (enemy.get_rect()[0] + 110, enemy.get_rect()[1] + 7))  # Рендеринг изображений
        self.sc.blit(heart, (diam.get_rect()[0] + 60, diam.get_rect()[1] + 10))
        self.sc.blit(diam, diam.get_rect())

    def set_params(self, hp, diam, enemies):  # Изменение параметров счетчика
        self.hp = hp
        self.diamonds = diam
        self.enemies = enemies
