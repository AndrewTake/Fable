import pygame
import sys
from settings import *
from world import World


class Game:
    """ Represents the game """

    def __init__(self):
        """ Initializes the game setup """
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Fable')
        self.clock = pygame.time.Clock()

        self.level = World()

    def run(self):
        """ Runs the game """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
