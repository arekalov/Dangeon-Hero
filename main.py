import os
import random

import pygame as pg
import sys

import pygame.display
from pygame.sprite import Sprite

W = 1000
H = 510
sc = pg.display.set_mode((W, H))
clock = pygame.time.Clock()
fps = 60


def load_image(name, colorkey=None):
    fullname = os.path.join('data/textures', name)
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


tile_images = {
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
    'thorn': load_image('thorn.png')
}
# player_image = load_image('mario.png')
tile_width, tile_height = 23, 23

tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '0':
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
            elif level[y][x] == 'f':
                Tile('flowers', x, y)
            elif level[y][x] == 'l':
                Tile('ladder', x, y)
            elif level[y][x] == 't':
                Tile('thorn', x, y)
    #         elif level[y][x] == '@':
    #             Tile('empty', x, y)
    #             new_player = Player(x, y)
    # # вернем игрока, а также размер поля в клетках
    return x, y


level_x, level_y = generate_level(load_level('level.txt'))

while 1:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
    pygame.display.flip()
    sc.fill((0, 0, 0))
    all_sprites.draw(sc)
    clock.tick(fps)
