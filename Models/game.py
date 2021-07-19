import sys
import pygame
from os.path import join
from Models.player import Player
from Models.enemy import Enemy
from Models.utils import Utils
from Models.coin import Coin
from Models.maze import Maze

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((Utils.WIDTH, Utils.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = Utils.MAZE_WIDTH // Utils.COLS
        self.cell_height = Utils.MAZE_HEIGHT // Utils.ROWS
        self.walls = []
        self.coins = []
        self.enemies = []
        self.e_pos = []
        self.p_pos = None
        maze = Maze(self)
        maze.load()
        self.player = Player(self, vec(self.p_pos))

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(Utils.FPS)
        pygame.quit()
        sys.exit()

    # HELPER FUNCTIONS
    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.coins = []
        with open(join("Assets", "walls.txt"), 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == 'C':
                        self.coins.append(vec(xidx, yidx))
        self.state = "playing"

    # INTRO FUNCTIONS
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = 'playing'

    def start_draw(self):
        self.screen.fill(Utils.BLACK)
        Utils.draw_text('PUSH SPACE BAR', self.screen, [
            Utils.WIDTH // 2, Utils.HEIGHT // 2 - 50], Utils.START_TEXT_SIZE, (170, 132, 58), Utils.START_FONT,
                        centered=True)
        Utils.draw_text('1 PLAYER ONLY', self.screen, [
            Utils.WIDTH // 2, Utils.HEIGHT // 2 + 50], Utils.START_TEXT_SIZE, (44, 167, 198), Utils.START_FONT,
                        centered=True)
        Utils.draw_text('HIGH SCORE', self.screen, [4, 0],
                        Utils.START_TEXT_SIZE, (255, 255, 255), Utils.START_FONT)
        pygame.display.update()

    # PLAYING FUNCTIONS

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
        self.screen.fill(Utils.BLACK)
        self.screen.blit(self.background, (Utils.TOP_BOTTOM_BUFFER // 2, Utils.TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        # self.draw_grid()
        Utils.draw_text('CURRENT SCORE: {}'.format(self.player.current_score),
                        self.screen, [60, 0], 18, Utils.WHITE, Utils.START_FONT)
        Utils.draw_text('HIGH SCORE: 0', self.screen, [Utils.WIDTH // 2 + 60, 0], 18, Utils.WHITE, Utils.START_FONT)
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0

    def draw_coins(self):
        for coin in self.coins:
            coin.draw(self.screen)

    # GAME OVER FUNCTIONS

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_draw(self):
        self.screen.fill(Utils.BLACK)
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        Utils.draw_text("GAME OVER", self.screen, [Utils.WIDTH // 2, 100], 52, Utils.RED, "arial", centered=True)
        Utils.draw_text(again_text, self.screen, [
            Utils.WIDTH // 2, Utils.HEIGHT // 2], 36, (190, 190, 190), "arial", centered=True)
        Utils.draw_text(quit_text, self.screen, [
            Utils.WIDTH // 2, Utils.HEIGHT // 1.5], 36, (190, 190, 190), "arial", centered=True)
        pygame.display.update()
