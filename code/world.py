import pygame
from settings import *
from tile import Tile
from character import Character
from support import *
from random import choice
from ui import UI


class World:
    """ Represents the world of the character """

    def __init__(self):
        """ Initializes the world """
    # get the display surface
        self.display_surface = pygame.display.get_surface()

    # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

    # sprite setup
        self.create_map()

    # user interface
        self.ui = UI()

    def create_map(self):
        """ Creates the world map """
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv'),
        }
        graphics = {
            'grass': import_folder('../graphics/Grass'),
            'objects': import_folder('../graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [
                                self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)

                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites,
                                          self.obstacle_sprites], 'object', surf)

            self.character = Character(
                (800, 650), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        """ Runs the map """
        # update and draw the game
        self.visible_sprites.custom_draw(self.character)
        self.visible_sprites.update()
        self.ui.display(self.character)


class YSortCameraGroup(pygame.sprite.Group):
    """ Creates a camera angle for the character """

    def __init__(self):
        """ Initializes the camera angle for the character """

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load(
            '../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, character):
        """ Draws the character and centers them on the map """

        # getting the offset
        self.offset.x = character.rect.centerx - self.half_width
        self.offset.y = character.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
