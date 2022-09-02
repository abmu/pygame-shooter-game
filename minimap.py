import pygame
from settings import *
from tile_mini import TileMini


class Minimap():
    def __init__(self,visible_sprites,map_size):
        # minimap setup
        self.screen = pygame.display.get_surface()
        self.visible_sprites = visible_sprites
        self.minimap_sprites = pygame.sprite.Group()
        self.map_size = self.get_minimap_size(map_size)

    def get_minimap_size(self,map_size):
        map_x = map_size[0]//64 * TILE_MINI_SIZE
        map_y = map_size[1]//64 * TILE_MINI_SIZE
        return (map_x,map_y)

    def draw_rect(self):
        # draw transparent background rectangle
        rect = pygame.Surface(self.map_size)
        rect.set_alpha(240)
        rect.fill(COLOUR_2)
        self.screen.blit(rect,(20,HEIGHT-self.map_size[1]-20))

    def update_minimap(self):
        for sprite in self.visible_sprites:
            # exclude particular sprites from the minimap
            # accept tiles, players, enemies, bullets, coins
            if sprite.__class__.__name__ in ('Tile','Player','Enemy','Bullet','Coin','Food'): 
                # check if the sprite has already been added to the minimap
                if sprite.drawn_mini == False:
                    sprite.drawn_mini = True
                    x = (sprite.rect.x // TILE_SIZE) * TILE_MINI_SIZE
                    y = (sprite.rect.y // TILE_SIZE) * TILE_MINI_SIZE
                    TileMini((x,y),[self.minimap_sprites],sprite,self.map_size)

    def display(self):
        # update minimap
        self.update_minimap()
        self.draw_rect()
        self.minimap_sprites.draw(self.screen)
        self.minimap_sprites.update()