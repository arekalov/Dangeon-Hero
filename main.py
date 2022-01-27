import sys
import pygame
from Camera import Camera, camera_configure
from Enemies import DynamicEnemy, StaticEnemy
from Hero import Hero
from StatusBar import StatusBar
from Tile import Tile
from hello import hello
from load_functions import load_image, load_level
from sprites_data import player_group, enemies_group, all_sprites, tile_height, tile_width, tiles_group, \
    decorations_group, fires_group
from pause_window import pause
from game_over import game_over


def terminate():
    pygame.quit()
    sys.exit()


def level_render(W, H, sc, map):
    clock = pygame.time.Clock()
    fps = 60
    left, right, up = False, False, False
    COLOR = "#201a34"
    pygame.display.set_caption('Dangeon Hero')
    pygame.init()

    def generate_level(level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == 'H':
                    Hero(x, y)
                elif level[y][x] == 'e':
                    DynamicEnemy(x, y)
                elif level[y][x] == 'w':
                    StaticEnemy(x, y)
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
        return x, y, level

    def killer():
        for i in player_group:
            i.kill()
        for i in enemies_group:
            i.kill()
        for i in all_sprites:
            i.kill()
        for i in tiles_group:
            i.kill()
        for i in decorations_group:
            i.kill()
        for i in fires_group:
            i.kill()

    stbar = StatusBar(3, sc)
    level_x, level_y, levvel = generate_level(load_level(map))
    total_level_width = len(levvel[0]) * tile_width  # Высчитываем фактическую ширину уровня
    total_level_height = len(levvel) * tile_height  # высоту

    bacgr = load_image('background1.png')
    camera = Camera(camera_configure, total_level_width, total_level_height)
    pygame.mouse.set_visible(False)
    while 1:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.mouse.set_visible(True)
                terminate()
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
            if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                pygame.mouse.set_visible(True)
                up, left, right = False, False, False
                callback = pause(W, H, sc)
                if callback == 'menu':
                    killer()
                    return 'stop'
                elif callback == 'restart':
                    killer()
                    return map
                pygame.mouse.set_visible(False)
        pygame.display.flip()
        sc.blit(bacgr, (0, 0))
        for e in all_sprites:
            sc.blit(e.image, camera.apply(e))
        for i in player_group:
            if i.hp == 0:
                game_over(W,H, sc, 'game_over.png')
                killer()
                pygame.mouse.set_visible(True)
                return 'stop'
            stbar.set_params(i.hp, i.diamonds_count, i.kills)
            camera.update(i)
        for i in player_group:
            if i.win:
                game_over(W, H, sc, 'win.png', (stbar.enemies, stbar.diamonds))
                killer()
                pygame.mouse.set_visible(True)
                return 'stop'
            if i.read:
                print(i.read)
                hello(W, H, sc, 'hello.png')
                i.read = False
                killer()
                pygame.mouse.set_visible(True)
                return 'stop'

        stbar.draw()
        player_group.update(left, right, up)
        enemies_group.update()
        clock.tick(fps)

# W = 1000
# H = 510
# sc = pygame.display.set_mode((W, H))
# level_render(1000, 510, sc, 'level.txt')
