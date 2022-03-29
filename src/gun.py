import pygame
import math
import game



def special_division(f,s):
  return f/s if s else 0


class Gun(pygame.sprite.Sprite):
    def __init__(self):
        self.speed = 15
        self.isShooting = False
        self.bullets = []
        self.idCount = 0
        super().__init__()

    
    def create(self,startpos,endpos):
        surf = pygame.Surface((3,3))
        surf.fill((0,0,0))
        initialpos = startpos
        endpos = endpos
        rect = surf.get_rect(
            center=initialpos
        )
    

        self.bullets.append({
          "id": self.idCount,
          "surf": surf,
          "initialpos": initialpos,
          "endpos":endpos,
          "rect": rect
        })
        self.idCount += 1

    def delete(self,bullet):
      print(bullet)
      for index in range(len(self.bullets)):
        if self.bullets[index]['id'] == bullet["id"]:
          del self.bullets[index]
          break


    def shooting(self,events=[]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.isShooting = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.isShooting = False

    def prune(self):
        #Gets rid of all bullets not on screen
        for bullet in self.bullets:
            if bullet["rect"].top <= 0 or bullet["rect"].bottom >= game.Game.BOARD_HEIGHT or bullet["rect"].left <= 0 or bullet["rect"].right >= game.Game.BOARD_WIDTH:
                self.delete(bullet)
    
    def update(self):
        #Moves position along X axis
      
        for bullet in self.bullets:
            initialpos = bullet["initialpos"]
            endpos = bullet["endpos"]
            angle = math.atan2(endpos[1]-initialpos[1],endpos[0]-initialpos[0])
            dx = self.speed*math.cos(angle)
            dy = self.speed*math.sin(angle)

            bullet["rect"].move_ip(dx,dy)          
            
            game.Game.screen.blit(bullet["surf"],bullet["rect"])
        
        self.prune()

        #Find slope of each bullet and advance in that direction by the speed value
