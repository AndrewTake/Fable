from ast import Pass
import pygame
from settings import *


class UI:
    def __init__(self) -> None:

        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        # bar setup
        self.stanima_bar_rect = pygame.Rect(
            10, 34, BAR_WIDTH, BAR_HEIGHT)
        self.health_bar_rect = pygame.Rect(
            10, 10, BAR_WIDTH, BAR_HEIGHT)
        self.power_bar_rect = pygame.Rect(
            10, 58, POWER_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current_amount, max_amount, background_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, background_rect)

        # converting stats to pixel
        ratio = current_amount / max_amount
        current_width = background_rect.width * ratio
        current_rect = background_rect.copy()
        current_rect.width = current_width
        # draw bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface,
                         UI_BORDER_COLOR, background_rect, 3)

    def show_exp(self, exp):
        text_surface = self.font.render(str(int(exp)), False, TEXT_COLOR)
    #    choosing location for the experience
        x = self.display_surface.get_size()[0] - 30
        y = self.display_surface.get_size()[1] - 670
        text_rect = text_surface.get_rect(bottomright=(x, y))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         text_rect.inflate(20, 20))
        self.display_surface.blit(text_surface, text_rect)

        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         text_rect.inflate(20, 20), 3)

    def display(self, character):
        # pygame.draw.rect(self.display_surface, 'black', self.health_bar_rect)
        self.show_bar(
            character.health, character.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(
            character.stanima, character.stats['stanima'], self.stanima_bar_rect, STANIMA_COLOR)
        self.show_bar(
            character.power, character.stats['power'], self.power_bar_rect, POWER_COLOR)
        self.show_exp(character.exp)
