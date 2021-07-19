import pygame
from pygame.math import Vector2 as vec
from Models.utils import Utils


class Coin:
    def __init__(self, app, x, y):
        self.pos = vec(x, y)
        self.app = app

    def draw(self, screen):
        pygame.draw.circle(screen, (124, 123, 7),
                           (int(self.pos.x * self.app.cell_width) + self.app.cell_width //
                            2 + Utils.TOP_BOTTOM_BUFFER // 2,
                            int(self.pos.y * self.app.cell_height) + self.app.cell_height //
                            2 + Utils.TOP_BOTTOM_BUFFER // 2),
                           5)
