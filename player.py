import pygame
from board import Board
from gun import Gun
class Player(pygame.sprite.Sprite,Board):
    def __init__(self,pos):
        super().__init__()
        self.surf = pygame.Surface((25,25))
        self.surf.fill((0,0,0))
        Player.rect = self.surf.get_rect(
            center=pos
        )
        self.speed = 10
        Player.gun = Gun()

    def move(self,pressed_keys):
        if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0,-self.speed)
        if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0,self.speed)
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed,0)
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed,0)

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.BOARD_HEIGHT:
            self.rect.bottom = self.BOARD_HEIGHT
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.BOARD_WIDTH:
            self.rect.right = self.BOARD_WIDTH
