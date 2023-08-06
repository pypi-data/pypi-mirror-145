import pygame
from pgzero.rect import Rect
from pgzero.screen import Screen


# Dialog stores simple data like lines to display and width of dialog
class Dialog:
    # Color (x,y,z) -> numbers from 0 to 255
    def __init__(self, lines, width, color):
        self.lines = lines
        self.width = width
        self.color = color

    def draw(self, screen):
        Dialog.draw_dialog(self.lines, screen=screen, width=self.width, color=self.color)

    # Drawing dialog, dialog height may differ as the items length differs
    @staticmethod
    def draw_dialog(lines, screen: Screen, active_position=-1, width=14, color=(0, 255, 0)):
        def draw_horizontal_border(height, width_of_dialog, border_color):
            screen.draw.filled_rect(
                Rect((screen.width / 2 - ((width_of_dialog // 2 + 1) * 32), height - 32),
                     (((width_of_dialog + 2) * 32), 32)), border_color)

            image = pygame.transform.rotate(pygame.image.load("images/dialog_end.png"), 90)
            screen.blit(image, (screen.width / 2 - ((width_of_dialog // 2 + 1) * 32), height - 32))
            screen.blit(pygame.image.load("images/dialog_cross.png"), (screen.width / 2 - ((width_of_dialog // 2) * 32), height - 32))
            for i in range((width_of_dialog - 2) // 2):
                image = pygame.transform.rotate(pygame.image.load("images/dialog_middle.png"), 90)
                screen.blit(image, (screen.width / 2 - ((i + 1) * 32), height - 32))
                screen.blit(image, (screen.width / 2 + (i * 32), height - 32))
            screen.blit(pygame.image.load("images/dialog_cross.png"),
                        (screen.width / 2 + (((width_of_dialog // 2) - 1) * 32), height - 32))
            image = pygame.transform.rotate(pygame.image.load("images/dialog_start.png"), 90)
            screen.blit(image, (screen.width / 2 + ((width_of_dialog // 2) * 32), height - 32))

        width_of_dialog = width
        height_of_dialog = screen.height / 2

        draw_horizontal_border(height_of_dialog, width_of_dialog, color)

        for i in range(len(lines)):
            screen.draw.filled_rect(
                Rect((screen.width / 2 - ((width_of_dialog // 2) * 32), height_of_dialog + (i * 32)), (32,32)),
                color)
            image = pygame.transform.rotate(pygame.image.load("images/dialog_middle.png"), 180)
            screen.blit(image, (screen.width / 2 - ((width_of_dialog // 2) * 32), height_of_dialog + (i * 32)))
            screen.draw.filled_rect(
                Rect((screen.width / 2 - ((width_of_dialog // 2 - 1) * 32), height_of_dialog + (i * 32)),
                     ((width_of_dialog - 2) * 32, 32)),
                (0, 0, 0))

            screen.draw.text(str(lines[i]), fontname="dizzy-iii-fantasy-world-dizzy-spectrum", fontsize=16,
                             centerx=screen.width / 2, top=height_of_dialog + (i * 32) + 8,
                             color=(0, 0, 255) if active_position == i else (255, 255, 255))

            screen.draw.filled_rect(
                Rect((screen.width / 2 + (width_of_dialog//2 - 1) * 32, height_of_dialog + (i * 32)), (32, 32)),
                color)
            screen.blit(pygame.image.load("images/dialog_middle.png"),
                        (screen.width / 2 + (width_of_dialog//2 - 1) * 32, height_of_dialog + (i * 32)))

        draw_horizontal_border(height_of_dialog + (len(lines) + 1) * 32, width_of_dialog, color)
