import pygame
from pgzero.rect import Rect
from pgzero.screen import Screen



class Hud:
    def __init__(self, lives, hp_percentage):
        self.lives = lives
        self.hp_percentage = hp_percentage



    def draw(self, screen: Screen, title: str):
        self.show_lives(screen, self.hp_percentage, self.lives)
        screen.draw.text(title.replace("_", "-"), fontname="dizzy-iii-fantasy-world-dizzy-spectrum",
                               fontsize=24, top=4 * 32, centerx=32 * 32 / 2)

    def show_lives(self, screen: Screen, percentage: int, lives: int):

        for i in range(lives):
            screen.blit(pygame.image.load('images/health_icon.png'), pos=(i * 48 + 32, 32))

        width = 23 * 32
        height = 1 * 32

        size_of_red_rect = size_of_yellow_rect = 64
        size_of_green_rect = 128

        border_rect = Rect((width-2, height-2), (2 + size_of_red_rect + size_of_yellow_rect + size_of_green_rect, 36))
        screen.draw.rect(border_rect, (0, 0, 200))

        # GREEN is 50% of the bar
        if percentage > 50:
            value_to_show = 100 / (50 / (percentage - 50))
            GREEN = 0, 200, 0
            BOX = Rect((width + size_of_red_rect + size_of_yellow_rect, height),
                       (size_of_green_rect / 100 * value_to_show, 32))
            screen.draw.filled_rect(BOX, GREEN)
            percentage = 50

        # YELLOW is 25% of the bar
        if percentage > 25:
            value_to_show = 100 / (25 / (percentage - 25))
            YELLOW = 200, 200, 0
            BOX = Rect((width + size_of_red_rect, height), (size_of_yellow_rect / 100 * value_to_show, 32))
            screen.draw.filled_rect(BOX, YELLOW)
            percentage = 25

        # RED is 25% of the bar
        if percentage > 0:
            value_to_show = 100 / (25 / percentage)
            RED = 200, 0, 0
            BOX = Rect((width, height), (size_of_red_rect / 100 * value_to_show, 32))
            screen.draw.filled_rect(BOX, RED)