import pygame

from sprites_data import all_sprites, diamonds_group, ladders_group, billboards_group, decorations_group, fires_group, \
    chests_group, tiles_group, tile_images, tile_width, tile_height, opened_chests_group


class Tile(pygame.sprite.Sprite):  # Все тайлы кроме персонажей и врагов
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        # Блок проверки причастия тайла к определенному типу и добавление в группы спрайтов
        if tile_type == 'diamond':
            self.add(diamonds_group)
        elif tile_type == 'ladder':
            self.add(ladders_group)
        elif tile_type == 'billboard':
            self.add(billboards_group)
        elif tile_type == 'flowers':
            self.add(decorations_group)
        elif tile_type == 'lava':
            self.add(fires_group)
        elif tile_type == 'fire':
            self.add(fires_group)
        elif tile_type == 'chest':
            self.add(chests_group)
        elif tile_type == 'opened_chest':
            self.add(opened_chests_group)
        elif tile_type == 'lava' or tile_type == 'fire' or tile_type == 'thorn':
            self.add(fires_group)
        else:
            self.add(tiles_group)
        self.image = tile_images[tile_type]  # Подгрузка базового спрайта
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
