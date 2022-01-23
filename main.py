import os
import sys

import pygame
import pyganim as pyganim
from pygame import sprite

clock = pygame.time.Clock()
fps = 60
left, right, up = False, False, False

W = 1000
H = 510
COLOR = "#000000"


def load_image(name, colorkey=None):
    fullname = os.path.join('data/sprites', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + W / 2, -t + H / 1.5

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - W), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - H), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


tiles_group = pygame.sprite.Group()
ladders_group = pygame.sprite.Group()
diamonds_group = pygame.sprite.Group()
billboards_group = pygame.sprite.Group()
decorations_group = pygame.sprite.Group()
fires_group = pygame.sprite.Group()
chests_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()

ANIMATION_DELAY = 1  # скорость смены кадров
ANIMATION_WALK_R = [('data/sprites/Hero/Walk_r/walk1.png'),
                    ('data/sprites/Hero/Walk_r/walk2.png'),
                    ('data/sprites/Hero/Walk_r/walk3.png'),
                    ('data/sprites/Hero/Walk_r/walk4.png')]

ANIMATION_WALK_L = [('data/sprites/Hero/Walk_l/walk1.png'),
                    ('data/sprites/Hero/Walk_l/walk2.png'),
                    ('data/sprites/Hero/Walk_l/walk3.png'),
                    ('data/sprites/Hero/Walk_l/walk4.png')]

ANIMATION_JUMP_R = [('data/sprites/Hero/Jump_r/jump1.png'),
                    ('data/sprites/Hero/Jump_r/jump2.png'),
                    ('data/sprites/Hero/Jump_r/jump3.png'),
                    ('data/sprites/Hero/Jump_r/jump4.png')]

ANIMATION_JUMP_L = [('data/sprites/Hero/Jump_l/jump1.png'),
                    ('data/sprites/Hero/Jump_l/jump2.png'),
                    ('data/sprites/Hero/Jump_l/jump3.png'),
                    ('data/sprites/Hero/Jump_l/jump4.png')]

ANIMATION_STAY = [('data/sprites/Hero/Walk_r/walk1.png', ANIMATION_DELAY)]
ANIMATION_FIGHT = [('data/sprites/Hero/Fight/fight1.png'),
                   ('data/sprites/Hero/Fight/fight2.png')]
ANIMATION_CLIMB = [('data/sprites/Hero/Climb/climb1.png', ANIMATION_DELAY)]


class Hero(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.MOVESPEED = 3
        self.JUMPPOWER = 6
        self.onLadder = False
        self.GRAVITY = 0.35
        self.yvel = 0
        self.onGround = False
        self.image = tile_images['player']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + -20)
        self.diamonds_count = 0

        # self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        #        Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_WALK_R:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimWalk_R = pyganim.PygAnimation(boltAnim)
        self.boltAnimWalk_R.play()
        #        Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_WALK_L:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimWalk_L = pyganim.PygAnimation(boltAnim)
        self.boltAnimWalk_L.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimClimb = pyganim.PygAnimation(ANIMATION_CLIMB)
        self.boltAnimClimb.play()

        boltAnim = []
        for anim in ANIMATION_JUMP_R:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimJump_R = pyganim.PygAnimation(boltAnim)
        self.boltAnimJump_R.play()

        boltAnim = []
        for anim in ANIMATION_JUMP_L:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimJump_L = pyganim.PygAnimation(boltAnim)
        self.boltAnimJump_L.play()

        boltAnim = []
        for anim in ANIMATION_FIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimFight = pyganim.PygAnimation(boltAnim)
        self.boltAnimFight.play()

    def update(self, left, right, up):
        if left:
            self.xvel = -self.MOVESPEED  # Лево = x- n
            if up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJump_L.blit(self.image, (0, 0))
            else:
                self.boltAnimWalk_L.blit(self.image, (0, 0))

        if right:
            self.xvel = self.MOVESPEED  # Право = x + n
            if up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJump_R.blit(self.image, (0, 0))
            else:
                self.boltAnimWalk_R.blit(self.image, (0, 0))
        if up:
            if self.onGround and not self.onLadder:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -self.JUMPPOWER
                self.boltAnimJump_R.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(pygame.Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))
        if self.onLadder:
            self.boltAnimStay.blit(self.image, (0, 0))
        if not self.onGround and not self.onLadder:
            self.yvel += self.GRAVITY
        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel)
        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0)
        self.onLadder = False

    def collide(self, xvel, yvel):
        if sprite.spritecollideany(self, diamonds_group):
            diamond = sprite.spritecollideany(self, diamonds_group)
            self.diamonds_count += 1
            diamond.kill()
            print(self.diamonds_count)
        elif sprite.spritecollideany(self, ladders_group):
            ladder = sprite.spritecollideany(self, ladders_group)
            self.onGround = True
            self.onLadder = True
            self.boltAnimStay.blit(self.image, (0, 0))
            if up:
                self.rect.x = ladder.rect.x

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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        if tile_type == 'diamond':
            self.add(diamonds_group)
        elif tile_type == 'ladder':
            self.add(ladders_group)
        elif tile_type == 'billboard':
            self.add(billboards_group)
        elif tile_type == 'flowers':
            self.add(decorations_group)
        elif tile_type == 'chest' or tile_type == 'opened_chest':
            self.add(chests_group)
        elif tile_type == 'lava' or tile_type == 'fire' or tile_type == 'thorn':
            self.add(fires_group)
        else:
            self.add(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


ENEMY_ANIMATION_WALK_R = [('data/sprites/SimpleEnemy/r/enemy1.png'),
                          ('data/sprites/SimpleEnemy/r/enemy2.png')]
ENEMY_ANIMATION_WALK_L = [('data/sprites/SimpleEnemy/l/enemy1.png'),
                           ('data/sprites/SimpleEnemy/l/enemy2.png')]


class DynamicEnemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super(DynamicEnemy, self).__init__(all_sprites, enemies_group)
        self.MOVESPEED = 3
        self.GRAVITY = 0.35
        self.hp = 1
        self.damage = 1
        self.image = tile_images['dyn_enemy']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + -10)
        self.radius_stop = 5
        self.radius_now = 0

        boltAnim = []
        for anim in ENEMY_ANIMATION_WALK_R:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimEnemy_walk_r = pyganim.PygAnimation(boltAnim)
        self.boltAnimEnemy_walk_r.play()
        #        Анимация движения влево
        boltAnim = []
        for anim in ENEMY_ANIMATION_WALK_L:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimEnemy_walk_l = pyganim.PygAnimation(boltAnim)
        self.boltAnimEnemy_walk_l.play()

    def update(self):
        # if self.radius_now + 1 >= self.radius_stop:
        #     self.MOVESPEED = -self.MOVESPEED
        #     self.radius_now = 0
        # self.radius_now += 1
        # self.rect.move(self.MOVESPEED, 0)
        # if self.MOVESPEED > 0:
        #     self.boltAnimEnemy_walk_r.blit(self.image, (0, 0))
        # else:
        #     self.boltAnimEnemy_walk_l.blit(self.image, (0, 0))
        if not pygame.sprite.spritecollideany(self, tiles_group):
            self.rect.y = self.rect.y + self.GRAVITY

levvel = []


def generate_level(level):
    global levvel
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'H':
                Hero(x, y)
            elif level[y][x] == 'e':
                DynamicEnemy(x, y)
            elif level[y][x] == '0':
                Tile('left_block', x, y)
            elif level[y][x] == '9':
                Tile('right_block', x, y)
            elif level[y][x] == '1':
                Tile('bwg1', x, y)
            elif level[y][x] == 'u':
                Tile('und_block', x, y)
            elif level[y][x] == 'b':
                Tile('billboard', x, y)
            elif level[y][x] == '2':
                Tile('bwg2', x, y)
            elif level[y][x] == '3':
                Tile('bwg3', x, y)
            elif level[y][x] == 'c':
                Tile('chest', x, y)
            elif level[y][x] == 'o':
                Tile('opened_chest', x, y)
            elif level[y][x] == 'd':
                Tile('diamond', x, y)
            elif level[y][x] == 's':
                Tile('flowers', x, y)
            elif level[y][x] == 'l':
                Tile('ladder', x, y)
            elif level[y][x] == 't':
                Tile('thorn', x, y)
            elif level[y][x] == 'v':
                Tile('lava', x, y)
            elif level[y][x] == 'f':
                Tile('fire', x, y)
    levvel = level
    return x, y


sc = pygame.display.set_mode((W, H))
tile_width, tile_height = 23, 23
player_width, player_height = 21, 31

tile_images = {
    'player': load_image('hero-1.png'),
    'und_block': load_image('und_block.png'),
    'left_block': load_image('left_block.png'),
    'right_block': load_image('right_block.png'),
    'bwg1': load_image('block_with_green.png'),
    'billboard': load_image('billboard.png'),
    'bwg2': load_image('block_with_green2.png'),
    'bwg3': load_image('block_with_green3.png'),
    'chest': load_image('chest.png'),
    'opened_chest': load_image('opened_chest.png'),
    'diamond': load_image('diamond.png'),
    'flowers': load_image('flowers.png'),
    'ladder': load_image('ladder.png'),
    'thorn': load_image('thorn.png'),
    'lava': load_image('lava.png'),
    'fire': load_image('fire.png'),
    'dyn_enemy': load_image('enemy1.png')
}

level_x, level_y = generate_level(load_level('level.txt'))
total_level_width = len(levvel[0]) * tile_width  # Высчитываем фактическую ширину уровня
total_level_height = len(levvel) * tile_height  # высоту

camera = Camera(camera_configure, total_level_width, total_level_height)
while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        if i.type == pygame.KEYDOWN and i.key == pygame.K_UP:
            up = True
        if i.type == pygame.KEYUP and i.key == pygame.K_UP:
            up = False

        if i.type == pygame.KEYDOWN and i.key == pygame.K_RIGHT:
            right = True
        if i.type == pygame.KEYUP and i.key == pygame.K_RIGHT:
            right = False

        if i.type == pygame.KEYDOWN and i.key == pygame.K_LEFT:
            left = True
        if i.type == pygame.KEYUP and i.key == pygame.K_LEFT:
            left = False
    pygame.display.flip()
    sc.fill((0, 0, 0))
    for e in all_sprites:
        sc.blit(e.image, camera.apply(e))
    for i in player_group:
        camera.update(i)
    player_group.update(left, right, up)
    clock.tick(fps)
