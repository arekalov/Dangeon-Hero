import sys
import pygame
import pyganim
from pygame import sprite
from sprites_data import diamonds_group, player_group, ladders_group, tiles_group, enemies_group, fires_group, \
    all_sprites, tile_images, tile_height, tile_width, chests_group, opened_chests_group

COLOR = "#201a34"
ANIMATION_DELAY = 1  # скорость смены кадров
ANIMATION_WALK_R = ['data/sprites/Hero/Walk_r/walk1.png',  # Кадры для анимации движения направо
                    'data/sprites/Hero/Walk_r/walk2.png',
                    'data/sprites/Hero/Walk_r/walk3.png',
                    'data/sprites/Hero/Walk_r/walk4.png']

ANIMATION_WALK_L = ['data/sprites/Hero/Walk_l/walk1.png',  # Кадры для анимации движения налево
                    'data/sprites/Hero/Walk_l/walk2.png',
                    'data/sprites/Hero/Walk_l/walk3.png',
                    'data/sprites/Hero/Walk_l/walk4.png']

ANIMATION_JUMP_R = ['data/sprites/Hero/Jump_r/jump1.png',  # Кадры для анимации прыжка направо
                    'data/sprites/Hero/Jump_r/jump2.png',
                    'data/sprites/Hero/Jump_r/jump3.png',
                    'data/sprites/Hero/Jump_r/jump4.png']

ANIMATION_JUMP_L = ['data/sprites/Hero/Jump_l/jump1.png',  # Кадры для анимации прыжка налево
                    'data/sprites/Hero/Jump_l/jump2.png',
                    'data/sprites/Hero/Jump_l/jump3.png',
                    'data/sprites/Hero/Jump_l/jump4.png']

ANIMATION_STAY = [('data/sprites/Hero/Walk_r/walk1.png', ANIMATION_DELAY)]  # Кадр стояния игрока


class Hero(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.MOVESPEED = 3  # Скорость ходьбы
        self.JUMPPOWER = 6  # Дальность прыжка
        self.onLadder = False  # Флагна лестнице
        self.GRAVITY = 0.35  # Граитация
        self.danger = 1  # Урон персонажа
        self.hp = 3  # Жизни персонажа
        self.yvel = 0  # Перемещение по y
        self.win = False  # Дошел ли игрок до конца
        self.read = False
        self.onGround = False  # Флаг на Земле
        self.image = tile_images['player']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y)
        self.diamonds_count = 0  # Количество собранных алмазов
        self.invincibility = False  # Неуязввимость
        self.kills = 0  # Количество убийств врагов

        self.image.set_colorkey(pygame.Color(COLOR))  # делаем фон прозрачным
        # Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_WALK_R:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimWalk_R = pyganim.PygAnimation(boltAnim)
        self.boltAnimWalk_R.play()
        # Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_WALK_L:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimWalk_L = pyganim.PygAnimation(boltAnim)
        self.boltAnimWalk_L.play()
        # Анимация стояния
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим
        # Анимация прыжка вправо
        boltAnim = []
        for anim in ANIMATION_JUMP_R:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimJump_R = pyganim.PygAnimation(boltAnim)
        self.boltAnimJump_R.play()
        # Анимация прыжка влево
        boltAnim = []
        for anim in ANIMATION_JUMP_L:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimJump_L = pyganim.PygAnimation(boltAnim)
        self.boltAnimJump_L.play()

    def update(self, left, right, up):
        if left:
            self.xvel = -self.MOVESPEED  # Лево = x- n
            if up:  # Анимация вверх влево
                self.boltAnimJump_L.blit(self.image, (0, 0))
            else:  # Анимация влево
                self.boltAnimWalk_L.blit(self.image, (0, 0))

        if right:
            # Анимация вверх вправо
            self.xvel = self.MOVESPEED  # Право = x + n
            if up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJump_R.blit(self.image, (0, 0))
            else:  # Анимация вправо
                self.boltAnimWalk_R.blit(self.image, (0, 0))
        if up:  # Прыжок
            if self.onGround and not self.onLadder:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -self.JUMPPOWER
                self.boltAnimJump_R.blit(self.image, (0, 0))
        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(pygame.Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))
        if self.onLadder:  # Проверка стоит ли на лестнице
            self.boltAnimStay.blit(self.image, (0, 0))
        if not self.onGround and not self.onLadder:  # Гравитация
            self.yvel += self.GRAVITY
        self.onGround = False
        self.rect.y += self.yvel  # переносим свои положение на yvel
        self.collide(0, self.yvel, up)
        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, up)
        self.onLadder = False
        if self.invincibility:  # Если неуязвимость включена, отталкиваем героя от врага
            self.rect.x -= 80
            self.rect.y -= 40
            self.invincibility = False

    def collide(self, xvel, yvel, up):
        if sprite.spritecollideany(self, diamonds_group):  # Проверка на сбор алмазов
            diamond = sprite.spritecollideany(self, diamonds_group)
            self.diamonds_count += 1
            diamond.kill()

        if sprite.spritecollideany(self, enemies_group):  # Проверка на столкновение с врагом
            enemy = sprite.spritecollideany(self, enemies_group)
            if self.rect.bottom - 5 == enemy.rect.top:
                enemy.kill()
                self.kills += 1
            elif not self.invincibility:
                self.hp -= 1
                print(self.hp)
                self.invincibility = True

        elif sprite.spritecollideany(self, ladders_group):  # Проверка на нахождение на лестнице
            ladder = sprite.spritecollideany(self, ladders_group)
            self.onGround = True
            self.onLadder = True
            self.boltAnimStay.blit(self.image, (0, 0))
            if up:
                self.rect.x = ladder.rect.x

        elif sprite.spritecollideany(self, fires_group):  # Если герой упал
            self.hp = 0

        elif sprite.spritecollideany(self, chests_group):  # Если герой дошел до конца уровня
            self.win = True

        elif sprite.spritecollideany(self, opened_chests_group):  # Если герой дошел до конца уровня
            self.read = True

        elif not sprite.spritecollideany(self, opened_chests_group):  # Если герой дошел до конца уровня
            self.read = False

        if sprite.spritecollideany(self, tiles_group):
            tile = sprite.spritecollideany(self, tiles_group)  # если есть пересечение платформы с игроком
            if xvel > 0:  # если движется вправо
                self.rect.right = tile.rect.left  # то не движется вправо

            if xvel < 0:  # если движется влево
                self.rect.left = tile.rect.right  # то не движется влево

            if yvel > 0:  # если падает вниз
                self.rect.bottom = tile.rect.top  # то не падает вниз
                self.onGround = True  # и становится на что-то твердое
                self.yvel = 0  # и энергия падения пропадает

            if yvel < 0:  # если движется вверх
                self.rect.top = tile.rect.bottom  # то не движется вверх
                self.yvel = 0  # и энергия прыжка пропадает
