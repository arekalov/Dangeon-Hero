import pygame

W = 1000
H = 510


class Camera(object):  # Класс камеры
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):  # Конфигурация движения камеры
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + W / 2, -t + H / 1.5

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - W), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - H), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)
