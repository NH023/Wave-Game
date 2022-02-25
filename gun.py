import pygame
from board import Board
from player import Player
from fractions import Fraction



def special_division(f,s):
  return f/s if s else 0


class Gun(pygame.sprite.Sprite,Board):
    bullets = []
    isShooting = False
    mousepos = []
    def __init__(self):
        self.speed = 15
        super().__init__()

    
    def create(self):
        surf = pygame.Surface((3,3))
        surf.fill((0,0,0))
        playerpos = (Player.rect.centerx,Player.rect.centery)
        mousepos = pygame.mouse.get_pos()
        rect = surf.get_rect(
            center=playerpos
        )

        self.__class__.bullets.append({
          "surf": surf,
          "playerpos": playerpos,
          "mousepos":mousepos,
          "rect": rect
        })


    def shooting(self,events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                Gun.isShooting = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                Gun.isShooting = False

    def prune(self):
        #Gets rid of all bullets not on screen
        for bullet in self.__class__.bullets:
            if bullet["rect"].top <= 0 or bullet["rect"].bottom >= self.BOARD_HEIGHT or bullet["rect"].left <= 0 or bullet["rect"].right >= self.BOARD_WIDTH:
                self.__class__.bullets.remove(bullet)
    
    def update(self):
        #Moves position along X axis
      
        for bullet in self.__class__.bullets:

            playerpos = bullet["playerpos"]
            mousepos = bullet["mousepos"]
            rise = (mousepos[1] - playerpos[1])
            run = (mousepos[0] - playerpos[0])

            
          
            print(slope,other)
          
            bullet["rect"].move_ip(slope,other)

            
          
            
            self.screen.blit(bullet["surf"],bullet["rect"])

        #Find slope of each bullet and advance in that direction by the speed value
