import pygame
import pyganim

from sprites_data import tiles_group, player_group, tile_height, tile_width, tile_images, all_sprites, enemies_group

ENEMY_ANIMATION_WALK_R = ['data/sprites/SimpleEnemy/r/enemy1.png',  # Кадры для анимации движения направо
                          'data/sprites/SimpleEnemy/r/enemy2.png']
ENEMY_ANIMATION_WALK_L = ['data/sprites/SimpleEnemy/l/enemy1.png',  # Кадры для анимации движения налево
                          'data/sprites/SimpleEnemy/l/enemy2.png']

ANIMATION_DELAY = 1  # Скорость смены кадров
COLOR = "#201a34"  # Цвет заполнеения остатков спрайтов


class DynamicEnemy(pygame.sprite.Sprite):  # Движущийся враг
    def __init__(self, pos_x, pos_y):
        super(DynamicEnemy, self).__init__(all_sprites, enemies_group)
        self.MOVESPEED = 1  # Скорость врага
        self.GRAVITY = 1  # Гравитация
        self.hp = 1  # Здоровье врага
        self.damage = 1  # Урон врага
        self.image = tile_images['dyn_enemy']  # Базовый спрайт
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y)
        self.radius_stop = 100  # Область движения
        self.radius_now = 0
        # Анимация движения вправо
        boltAnim = []
        for anim in ENEMY_ANIMATION_WALK_R:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimEnemy_walk_r = pyganim.PygAnimation(boltAnim)
        self.boltAnimEnemy_walk_r.play()
        # Анимация движения влево
        boltAnim = []
        for anim in ENEMY_ANIMATION_WALK_L:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimEnemy_walk_l = pyganim.PygAnimation(boltAnim)
        self.boltAnimEnemy_walk_l.play()

    def update(self):
        # Блок проверки окончания области возможности ходьбы
        if self.radius_now + 1 >= self.radius_stop:
            self.MOVESPEED = -self.MOVESPEED
            self.radius_now = 0
        self.radius_now += 1
        self.rect.x += self.MOVESPEED
        if self.MOVESPEED > 0:
            self.image.fill(COLOR)
            self.boltAnimEnemy_walk_r.blit(self.image, (0, 0))
        else:
            self.image.fill(COLOR)
            self.boltAnimEnemy_walk_l.blit(self.image, (0, 0))
        # Проверка на нахождение на земле и гравитация
        if not pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y += self.GRAVITY


class StaticEnemy(pygame.sprite.Sprite):  # Статичный враг
    def __init__(self, pos_x, pos_y):
        super(StaticEnemy, self).__init__(all_sprites, enemies_group)
        self.GRAVITY = 1  # Гравитация
        self.hp = 1  # Жизни
        self.damage = 1  # Урон
        self.image = tile_images['dyn_enemy']  # Базовый спрайт
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y + -20)

    def update(self):  # Гравитация
        if not pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y += self.GRAVITY
