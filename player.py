import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        # player setup
        super().__init__(groups)
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()

        # change player direction
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self,speed):
        # normalize direction vector to ensure it is a unit vector
        # if direction vector is diagonal the magnitude > 1 <- not unit vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.y += self.direction.y * speed
        self.collision('vertical')        
        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        #self.rect.center += self.direction * speed

    def collision(self,direction):
        # handle vertical collisions
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom
                    elif self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top

        # handle horizontal collisons
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right
                    elif self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left 

    def update(self):
        # update player
        self.input()
        self.move(self.speed)