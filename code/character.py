import pygame
from settings import *
from support import import_folder


class Character(pygame.sprite.Sprite):
    """ Represents a character in the game """

    def __init__(self, pos, groups, obstacle_sprites):
        """ Initializes the character """
        super().__init__(groups)
        self.image = pygame.image.load(
            '../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # graphics setup
        self.import_character_assets()
        self.status = 'down'
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 200
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        # stats
        self.stats = {"health": 100, "stanima": 60, "attack": 10, "magic": 4,
                      "speed": 5, "power": 1}

        self.health = self.stats['health'] * 0.75
        self.stanima = self.stats['stanima'] * 0.75
        self.power = self.stats['power'] * 0.75
        self.exp = 123
        self.speed = self.stats['speed']

    def import_character_assets(self):
        """ Imports the character assets """
        character_path = '../graphics/player/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []
                           }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        """ Character input """
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            # attack input
            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('attack')

            # magic input
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print('magic')

    def get_status(self):
        """ Gets the status of the character """

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def move(self, speed):
        """ Moves the character """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """ Represents collisions for the character """
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        """ Cool down for character attacking """
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def animate(self):
        """ Animates the character """
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        """ Calls functions """
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
