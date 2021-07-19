import pygame


class Utils:
    # screen settings
    WIDTH, HEIGHT = 610, 670
    FPS = 60
    TOP_BOTTOM_BUFFER = 50
    MAZE_WIDTH, MAZE_HEIGHT = WIDTH - TOP_BOTTOM_BUFFER, HEIGHT - TOP_BOTTOM_BUFFER

    ROWS = 30
    COLS = 28

    # colour settings
    BLACK = (0, 0, 0)
    RED = (208, 22, 22)
    GREY = (107, 107, 107)
    WHITE = (255, 255, 255)
    PLAYER_COLOUR = (190, 194, 15)

    # font settings
    START_TEXT_SIZE = 16
    START_FONT = 'arial black'

    @staticmethod
    def draw_text(words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)
