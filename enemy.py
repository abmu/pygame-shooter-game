import pygame
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        # enemy setup
        super().__init__(groups)
        self.image = pygame.image.load('graphics/enemy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.draw_priority = 1
        self.start_pos = pos

        # movement
        self.direction = pygame.math.Vector2()
        self.player_distance = None
        self.obstacle_sprites = obstacle_sprites

        # attack
        self.attacking = False
        self.attack_cooldown = 1000
        self.attack_time = None

        # stats
        self.speed = 3
        self.max_health = 100
        self.health = self.max_health
        self.power = 10
        self.notice_radius = 500
        self.worth = 50

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
        # handle horizontal collisons with tiles and other enemies
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect) and sprite.__class__.__name__ in ('Tile','Enemy') and sprite.rect is not self.rect:
                    if self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right
                    elif self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left

        # handle vertical collisions with tiles and other enemies
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect) and sprite.__class__.__name__ in ('Tile','Enemy') and sprite.rect is not self.rect:
                    if self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom
                    elif self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top

    def calculate_player_distance_direction(self,player):
        # calculate player distance from enemy
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        self.player_distance = (player_vector-enemy_vector).magnitude()

        # check if enemy is touching player and not currently attacking
        if player.rect.colliderect(self.rect) and not self.attacking:
            player.take_damage(self.power)

            # begin attack cooldown
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
        # check if player is within the enemy's notice radius
        elif self.player_distance <= self.notice_radius:
            self.direction = (player_vector-enemy_vector)
        # make the enemy stop moving if there is no player within notice radius
        else:
            self.direction = pygame.math.Vector2()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # check if attack cooldown has finished
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def take_damage(self,power):
        self.health -= power
        if self.health <= 0:
            # make the enemy respawn once they die
            self.rect.topleft = self.start_pos
            self.health = self.max_health

    def get_worth(self):
        return self.worth

    def update(self):
        # upadte enemy
        self.cooldowns()
        self.move(self.speed)

    # method with access to the player object
    def enemy_update(self,player):
        self.calculate_player_distance_direction(player)