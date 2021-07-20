import pygame
from Models.utils import Utils
from Models.Entity import Entity
from os.path import join

vec = pygame.math.Vector2


class Player(Entity):
    def __init__(self, app, pos):
        super().__init__(app, pos)
        self.spritesup = []
        self.spritesdown = []
        self.spritesleft = []
        self.spritesright = []
        self.load_sprite()
        self.currentsprites = self.spritesright
        self.currentindex = 0
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = 3

    def update(self):
        self.set_sprite()
        self.animation()
        if self.able_to_move:
            self.pix_pos += self.direction * self.speed
        if self.time_to_move():
            if self.stored_direction is not None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()
        # Setting grid position in reference to pix pos
        self.grid_pos[0] = (self.pix_pos[0] - Utils.TOP_BOTTOM_BUFFER +
                            self.app.cell_width // 2) // self.app.cell_width + 1
        self.grid_pos[1] = (self.pix_pos[1] - Utils.TOP_BOTTOM_BUFFER +
                            self.app.cell_height // 2) // self.app.cell_height + 1
        self.on_coin()

    def draw(self):
        self.app.screen.blit(self.currentsprites[int(self.currentindex)], (int(self.pix_pos.x)-15,int(self.pix_pos.y)-20))

        # Drawing player lives
        for x in range(self.lives):
            pygame.draw.circle(self.app.screen, Utils.PLAYER_COLOUR, (30 + 20 * x, Utils.HEIGHT - 15), 7)

    def on_coin(self):
        for coin in self.app.coins:
            if self.grid_pos == coin.pos:
                if int(self.pix_pos.x + Utils.TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
                    if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                        self.eat_coin(coin)
                        return
                if int(self.pix_pos.y + Utils.TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
                    if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                        self.eat_coin(coin)
                        return

    def eat_coin(self, coin):
        self.current_score += 1
        self.app.coins.remove(coin)

    def move(self, direction):
        self.stored_direction = direction

    def time_to_move(self):
        if int(self.pix_pos.x + Utils.TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y + Utils.TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True
    
    def load_sprite(self):
        self.spritesright.append(pygame.image.load(join("Assets","pacright.png")))
        self.spritesright.append(pygame.image.load(join("Assets","pacright2.png")))
        self.spritesright.append(pygame.image.load(join("Assets","pacright3.png")))
        self.spritesup.append(pygame.image.load(join("Assets","pacup.png")))
        self.spritesup.append(pygame.image.load(join("Assets","pacup2.png")))
        self.spritesup.append(pygame.image.load(join("Assets","pacup3.png")))
        self.spritesleft.append(pygame.image.load(join("Assets","pacleft.png")))
        self.spritesleft.append(pygame.image.load(join("Assets","pacleft2.png")))
        self.spritesleft.append(pygame.image.load(join("Assets","pacleft3.png")))
        self.spritesdown.append(pygame.image.load(join("Assets","pacdown.png")))
        self.spritesdown.append(pygame.image.load(join("Assets","pacdown2.png")))
        self.spritesdown.append(pygame.image.load(join("Assets","pacdown3.png")))

    def animation(self):
        self.currentindex += 0.2
        if self.currentindex >= len(self.currentsprites):
            self.currentindex = 0

    def set_sprite(self):
        if self.direction == [1,0]:
            self.currentsprites = self.spritesright
        elif self.direction == [0,1]:
            self.currentsprites = self.spritesdown
        elif self.direction == [-1,0]:
            self.currentsprites = self.spritesleft
        elif self.direction == [0,-1]:
            self.currentsprites = self.spritesup
        