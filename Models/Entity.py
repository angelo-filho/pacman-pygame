from Models.utils import Utils
from pygame.math import Vector2 as vec


class Entity:
    def __init__(self, app, pos):
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(0, 0)
        self.speed = 0

    def get_pix_pos(self):
        return vec((self.grid_pos.x * self.app.cell_width) + Utils.TOP_BOTTOM_BUFFER // 2 + self.app.cell_width // 2,
                   (self.grid_pos.y * self.app.cell_height) + Utils.TOP_BOTTOM_BUFFER // 2 +
                   self.app.cell_height // 2)
