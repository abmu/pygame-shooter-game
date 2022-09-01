import pygame
import random
from pygame import mixer
from settings import *
from health_bar import HealthBar


class Enemy(pygame.sprite.Sprite):
    def __init__(self,spawn_positions,groups,obstacle_sprites,visible_sprites,sounds):
        # enemy setup
        super().__init__(groups)
        self.spawn_positions = spawn_positions
        self.last_pos = None
        self.image_1 = pygame.Surface((ENEMY_SIZE,ENEMY_SIZE)).convert_alpha()
        self.image_1.fill('green1')
        self.image_2 = pygame.Surface((ENEMY_SIZE,ENEMY_SIZE)).convert_alpha()
        self.image_2.fill('green4')
        self.image = self.image_1
        self.rect = self.image.get_rect(topleft = self.get_spawn_pos())
        self.draw_priority = 2

        # movement
        self.direction = pygame.math.Vector2()
        self.player_distance = None
        self.obstacle_sprites = obstacle_sprites

        # attack
        self.attacking = False
        self.attack_cooldown = 1000
        self.attack_time = None

        # hit
        self.hit = False
        self.hit_cooldown = 100
        self.hit_time = None

        # stats
        self.speed = 3
        self.max_health = 100
        self.health = self.max_health
        self.power = 10
        self.notice_radius = 500
        self.worth = 50

        self.health_bar = HealthBar(self.rect,self.get_health,[visible_sprites])

        # sound setup
        self.sounds = sounds

    def get_spawn_pos(self):
        # choose a random pos from the enemy pos dict
        # ensure that the pos is not taken and is not a None value
        spawn_pos = random.choice(list(self.spawn_positions.keys()))
        while self.spawn_positions[spawn_pos]: # self.spawn_positions[key] <- boolean value saying whether or not pos is currently taken
            spawn_pos = random.choice(list(self.spawn_positions.keys()))
            
        # make the previous pos occupied available and the current pos unavailable
        if self.last_pos is not None:
            self.spawn_positions[self.last_pos] = False
        self.spawn_positions[spawn_pos] = True
        self.last_pos = spawn_pos

        return spawn_pos

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

        # check if hit cooldown has finished
        if self.hit:
            if current_time - self.hit_time >= self.hit_cooldown:
                self.hit = False
                self.image = self.image_1

    def take_damage(self,power):
        if not self.hit:
            # load hit image
            self.image = self.image_2

            # make the enemy take damage
            self.health -= power
            if self.health <= 0:
                # make the enemy respawn once they die
                self.hit = False
                self.image = self.image_1
                self.rect.topleft = self.get_spawn_pos()
                self.health = self.max_health

            # begin hit cooldown
            self.hit = True
            self.hit_time = pygame.time.get_ticks()
            self.sounds.play('hit_ping')


    def get_worth(self):
        return self.worth

    def get_health(self):
        return (self.health,self.max_health)

    def update(self):
        # upadte enemy
        self.cooldowns()
        self.move(self.speed)

    # method with access to the player object
    def enemy_update(self,player):
        self.calculate_player_distance_direction(player)