import pygame
from pygame.math import Vector2 as vec
from os.path import join
from Models.utils import Utils
from Models.enemy import Enemy
from Models.coin import Coin


class Maze:
    def __init__(self, app):
        self.app = app

    def load(self):
        self.app.background = pygame.image.load(join("assets", "maze.png"))
        self.app.background = pygame.transform.scale(self.app.background, (Utils.MAZE_WIDTH, Utils.MAZE_HEIGHT))

        # Opening walls file
        # Creating walls list with co-ords of walls
        # stored as  a vector
        with open(join("assets", "walls.txt"), 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == "1":
                        self.app.walls.append(vec(xidx, yidx))
                    elif char == "C":
                        new_coin = Coin(self.app, xidx, yidx)
                        self.app.coins.append(new_coin)
                    elif char == "P":
                        self.app.p_pos = [xidx, yidx]
                    elif char in ["2", "3", "4", "5"]:
                        self.app.e_pos.append([xidx, yidx])
                        self.app.enemies.append(Enemy(self.app, vec(xidx, yidx), int(char) - 2))
                    elif char == "B":
                        pygame.draw.rect(self.app.background, Utils.BLACK, (xidx * self.app.cell_width, yidx *
                                                                            self.app.cell_height,
                                                                            self.app.cell_width, self.app.cell_height))
