import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites,create_bullet):
        # player setup
        super().__init__(groups)
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        # movement
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites

        # shooting
        self.pressed = False
        self.create_bullet = create_bullet
        self.attacking = False
        self.attack_cooldown = 200
        self.attack_time = None

        # stats
        self.speed = 5
        self.max_health = 100
        self.health = self.max_health
        self.points = 0

    def input(self):
        keys = pygame.key.get_pressed()

        # change player direction
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        # shoot bullet
        if pygame.mouse.get_pressed()[0] and not self.attacking: # check if lmb clicked
            self.pressed = True
        else:
            if self.pressed:
                self.create_bullet()
                self.pressed = False

                # begin attack cooldown
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

    def move(self,speed):
        # normalize direction vector to ensure it is a unit vector
        # if direction vector is diagonal the magnitude > 1 <- not unit vector
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')        

    def collision(self,direction):
        # handle horizontal collisons
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect) and sprite.__class__.__name__ == 'Tile':
                    if self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right
                    elif self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left

        # handle vertical collisions
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect) and sprite.__class__.__name__ == 'Tile':
                    if self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom
                    elif self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # check if attack cooldown has finished
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def get_health(self):
        return (self.health,self.max_health)

    def update(self):
        # update player
        self.input()
        self.cooldowns()
        self.move(self.speed)