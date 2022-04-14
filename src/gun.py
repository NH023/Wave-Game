import pygame
import math
import game
import random




def special_division(f,s):
  return f/s if s else 0

def distance_calculate(x1,y1,x2,y2):
  return math.sqrt(pow(x2-x1,2)+pow(y2-y1,2))

class Bullet():
  def __init__(self,id,pos,rect,direction,homing=False,bounce=False,pierce=False):
    self.id = id
    self.pos = pos
    self.rect = rect
    self.direction = direction
    self.speed = 15
    self.rect = rect
    self.homing = homing
    self.bounce = bounce
    self.pierce = pierce

  def get_self(self):
    return self

class Gun(pygame.sprite.Sprite):
    def __init__(self):
        self.isShooting = False
        self.bullets = []
        self.idCount = 0
        super().__init__()

    
    def create(self,initialpos,endpos,homing=False,bounce=False,pierce=False):
        
        pos = pygame.math.Vector2(initialpos)
        arctangent = math.atan2(endpos[1]-initialpos[1],endpos[0]-initialpos[0])
        dx = math.cos(arctangent)
        dy = math.sin(arctangent)
        direction = pygame.math.Vector2(dx,dy).normalize()
        surf = pygame.Surface((5,5))
        surf.fill((0,0,0))
        rect = surf.get_rect(
          center = initialpos
        )
        
        bullet = Bullet(self.idCount,pos,rect,direction,homing=homing,bounce=bounce,pierce=pierce)

        self.bullets.append(bullet)

        self.idCount += 1

      
  
    def delete(self,bullet):
      for index in range(len(self.bullets)):
        if self.bullets[index].id == bullet.id:
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
          if not bullet.bounce:
            if bullet.rect.top <= 0 or bullet.rect.bottom >= game.Game.BOARD_HEIGHT or bullet.rect.left <= 0 or bullet.rect.right >= game.Game.BOARD_WIDTH:
                self.delete(bullet)
    
    def clear(self):
      #Cleans all bullets off of the screen for next round
      self.bullets.clear()
        

    def update(self):
        #Moves position along X axis
        for bullet in self.bullets:

          #Homing Bullets WIP
          if bullet.homing:
            #Homing Missle/Bullet Shinangians
            #Find closest enemy to bullets current position

            target = None
            closest = 99999

            for instance in game.Game.WaveHandler.currentEnemies:
              EnemyX = instance.rect.x
              EnemyY = instance.rect.y
              dist = distance_calculate(EnemyX,EnemyY,bullet.rect.x,bullet.rect.y)
              if dist < closest:
                closest = dist
                target = instance
            
            
            print(bullet.direction)
            
            #Target is below bullet
            if bullet.rect.y > target.rect.y:
              bullet.direction[1] -= 0.1
              if bullet.direction[1] < -1:
                bullet.direction[1] = -1
            #Target is above bullet
            elif bullet.rect.y < target.rect.y:
              bullet.direction[1] += 0.1
              if bullet.direction[1] > 1:
                bullet.direction[1] = 1
            #Target is to the right of bullet
            if bullet.rect.x > target.rect.x:
              bullet.direction[0] -= 0.1
              if bullet.direction[0] < -1:
                bullet.direction[0] = -1
            #Target is to the left of bullet
            elif bullet.rect.x < target.rect.x:
              bullet.direction[0] += 0.1
              if bullet.direction[0] > 1:
                bullet.direction[0] = 1
            
            
          if bullet.bounce:
            if bullet.rect.left < 0 or bullet.rect.right > game.Game.BOARD_WIDTH:
              bullet.direction[0] = -bullet.direction[0]
            if bullet.rect.top < 0 or bullet.rect.bottom > game.Game.BOARD_HEIGHT:
              bullet.direction[1] = -bullet.direction[1]


          #If the bullet is a bullet - duh   
          bullet.pos += bullet.direction * bullet.speed
          bullet.rect.center = bullet.pos
          pygame.draw.rect(game.Game.screen,(255,0,0),bullet.rect)



            
        self.prune()


