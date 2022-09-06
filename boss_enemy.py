import pygame
from pygame import mixer
from settings import *
from enemy import Enemy
from health_bar import HealthBar
from level_text import LevelText


class BossEnemy(Enemy):
    def __init__(self,spawn_positions,groups,obstacle_sprites,visible_sprites,create_boss_bullet,sounds):
        # boss setup
        super().__init__(spawn_positions,groups,obstacle_sprites,visible_sprites,sounds)

        self.image_1 = pygame.Surface((BOSS_SIZE,BOSS_SIZE)).convert_alpha()
        self.image_1.fill('olivedrab1')
        self.image_2 = pygame.Surface((BOSS_SIZE,BOSS_SIZE)).convert_alpha()
        self.image_2.fill('olivedrab4')
        self.image = self.image_1
        self.rect = self.image.get_rect(topleft = self.get_spawn_pos())
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y

        # attack
        self.attack_radius = BOSS_SIZE/2 + PLAYER_SIZE/2 + 1
        self.create_boss_bullet = create_boss_bullet

        # update the health bar
        self.health_bar.change_rect(self.rect,self.get_health,BOSS_SIZE)
        # remove level from bosses
        self.level_text.kill()

    def update_stats(self,amount):
        # don't change stats once boss enemy dies
        self.max_speed = 2
        self.speed = self.max_speed
        self.max_health = 1000
        self.health = self.max_health
        self.power = 50
        self.notice_radius = 500
        self.worth = 300
        self.dead = False

    def calculate_player_distance_direction(self,player):
        # calculate player distance from enemy
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)
        self.player_distance = (player_vector-enemy_vector).magnitude()

        # attack if they player is within attack radius and enemy is not currently attacking
        if self.player_distance <= self.attack_radius and not self.attacking:
            # make the enemy stop moving if they collide with the player to stop them from passing through
            player.take_damage(self.power)
            if player.is_dead():
                player.update_stats()
                # decrease level if the enemy gets a kill
                self.update_stats(-1)

            # slow down speed
            self.speed -= 3 

            # begin attack cooldown
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
        # check if player is within the enemy's notice radius
        elif self.player_distance <= self.notice_radius:
            self.direction = (player_vector-enemy_vector)
            # shoot bullet
            if not self.attacking:
                self.sounds.play('shoot_ping')
                self.create_boss_bullet((self.rect.centerx-BOSS_BULLET_SIZE/2,self.rect.centery-BOSS_BULLET_SIZE/2),player_vector-enemy_vector,self.rect)

                # begin attack cooldown
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
        # make the enemy stop moving if there is no player within notice radius
        else:
            self.direction = pygame.math.Vector2()