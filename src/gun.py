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

    
    def create(self,initialpos,endpos):
        surf = pygame.Surface((3,3))
        surf.fill((0,0,0))
        rect = surf.get_rect(
            center=initialpos
        )
        arctangent = math.atan2(endpos[1]-initialpos[1],endpos[0]-initialpos[0])
        self.dx = self.speed*math.cos(arctangent)
        self.dy = self.speed*math.sin(arctangent)
        
    

        self.bullets.append({
          "id": self.idCount,
          "surf": surf,
          "initialpos": initialpos,
          "endpos":endpos,
          "rect": rect,
          "type": "standard"
        })
        self.idCount += 1

    def createHoming(self,initialpos,_target):
      surf = pygame.Surface((5,5))
      surf.fill((0,0,0))
      rect = surf.get_rect(
        center = initialpos
      ) 
      
      self.bullets.append({
        "id": self.idCount,
        "surf": surf,
        "initialpos": initialpos,
        "target": _target,
        "rect": rect,
        "type": "homing"
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
          if bullet["type"] == "standard":
            bullet["rect"].move_ip(self.dx,self.dy)                 
            game.Game.screen.blit(bullet["surf"],bullet["rect"])
          elif bullet["type"] == "homing":
            #Homing Missle/Bullet Shinangians
            
            targetX = pygame.mouse.get_pos()[0] - bullet["rect"].centerx
            targetY = pygame.mouse.get_pos()[1] - bullet["rect"].centery
            rotation = math.atan2(targetY, targetX) * 180 / math.pi
    #Velocity in x is relative to the angle, when it's 90&deg; or -90&deg;, vx should be 0.
            vx = self.speed * (90 - abs(rotation)) / 90
            if rotation < 0:
              vy = -self.speed + abs(vx)#Going upwards.
            else:
              vy = self.speed - abs(vx)#Going downwards.
     
            bullet["rect"].x += vx
            bullet["rect"].y += vy
            game.Game.screen.blit(bullet["surf"],bullet["rect"])
            
        self.prune()


