import pygame
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        # enemy setup
        super().__init__(groups)
        self.image = pygame.image.load('graphics/enemy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        # movement
        self.direction = pygame.math.Vector2()
        self.plaayer_distance = None
        self.obstacle_sprites = obstacle_sprites

        # attack
        self.attacking = False
        self.attack_cooldown = 1000
        self.attack_time = None

        # stats
        self.speed = 3
        self.max_health = 100
        self.health = self.max_health
        self.power = 20
        self.notice_radius = 100

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

    def calculate_player_distance_direction(self,player):
        # calculate player distance from enemy
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        self.distance = (player_vector-enemy_vector).magnitude()

        # check to see if enemy is already at the player
        # if they are then they shouldn't move 
        if self.distance > 0:
            self.direction = (player_vector-enemy_vector)
        else:
            self.direction = pygame.math.Vector2()

    def take_damage(self,power):
        self.health -= power
        if self.health <= 0:
            self.kill()

    def update(self):
        # upadte enemy
        self.move(self.speed)

    # method with access to the player object
    def enemy_update(self,player):
        self.calculate_player_distance_direction(player)