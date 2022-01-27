import pygame
from load_functions import load_image

tiles_group = pygame.sprite.Group()  # Группы спрайтов по категориям
ladders_group = pygame.sprite.Group()
diamonds_group = pygame.sprite.Group()
billboards_group = pygame.sprite.Group()
decorations_group = pygame.sprite.Group()
fires_group = pygame.sprite.Group()
chests_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
fires_groups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
opened_chests_group = pygame.sprite.Group()

tile_width, tile_height = 23, 23  # Размеры стандартных блоков
tile_images = {  # Спрайты подгруженнные из памяти
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
    'dyn_enemy': load_image('enemy1.png'),
    'damage1': load_image('damage1.png')
}
