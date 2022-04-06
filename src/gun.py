import pygame
import math
import game
import random



def special_division(f,s):
  return f/s if s else 0

def distance_calculate(x1,y1,x2,y2):
  return math.sqrt(pow(x2-x1,2)+pow(y2-y1,2))

class Bullet():
  def __init__(self,id,pos,rect,velocity,direction,type,initialpos=None,dx=None,dy=None,target=None,current_path=None):
    self.id = id
    self.pos = pos
    self.rect = rect
    self.velocity = velocity
    self.direction = direction
    self.rect = rect
    self.type = type
    #self.initialpos = initialpos
    #self.dx =dx
    #self.dy = dy
  def get_self(self):
    return self

class Gun(pygame.sprite.Sprite):
    def __init__(self):
        self.standard_velocity = 15
        self.isShooting = False
        self.bullets = []
        self.idCount = 0
        super().__init__()

    
    def create(self,initialpos,endpos):
        
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
        
        bullet = Bullet(self.idCount,pos,rect,self.standard_velocity,direction,type="standard")

        self.bullets.append(bullet)

        self.idCount += 1

    def createHoming(self,initialpos,_target,mousepos):
      
        pos = pygame.math.Vector2(initialpos)
        arctangent = math.atan2(mousepos[1]-initialpos[1],mousepos[0]-initialpos[0])
        dx = math.cos(arctangent)
        dy = math.sin(arctangent)
        direction = pygame.math.Vector2(dx,dy).normalize()
        surf = pygame.Surface((5,5))
        surf.fill((0,0,0))
        rect = surf.get_rect(
          center = initialpos
        )
        
        bullet = Bullet(self.idCount,pos,rect,self.standard_velocity,direction,type="homing")

        self.bullets.append(bullet)

        self.idCount += 1
      
  
    def delete(self,bullet):
      print(bullet)
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
            if bullet.rect.top <= 0 or bullet.rect.bottom >= game.Game.BOARD_HEIGHT or bullet.rect.left <= 0 or bullet.rect.right >= game.Game.BOARD_WIDTH:
                self.delete(bullet)
    
    def update(self):
        #Moves position along X axis
        for bullet in self.bullets:

          if bullet.type == "standard":

            bullet.pos += bullet.direction * bullet.velocity
            bullet.rect.center = bullet.pos
            pygame.draw.rect(game.Game.screen,(255,0,0),bullet.rect)







          elif bullet.type == "homing":
            #Homing Missle/Bullet Shinangians
            #Find closest enemy to bullets current position

            target = "enemy"
            closest = 100000000
            #bulletpos = (bullet.rect.x,bullet.rect.y)
            for instance in game.Game.WaveHandler.currentEnemies:
              EnemyX = instance.rect.x
              EnemyY = instance.rect.y
              dist = distance_calculate(EnemyX,EnemyY,bullet.rect.x,bullet.rect.y)
              if dist < closest:
                closest = dist
                target = instance
            
            
            print(bullet.direction)
            

            if bullet.rect.y > target.rect.y:
              bullet.direction[1] -= 0.1
              if bullet.direction[1] < -1:
                bullet.direction[1] = 0
            elif bullet.rect.y < target.rect.y:
              bullet.direction[1] += 1
              if bullet.direction[1] > 1:
                bullet.direction[1] = 0
            if bullet.rect.x > target.rect.x:
              bullet.direction[0] -= 1
              if bullet.direction[0] < -1:
                bullet.direction[0] = 0
            elif bullet.rect.x < target.rect.x:
              bullet.direction[0] += 1
              if bullet.direction[0] > 1:
                bullet.direction[0] = 0
            

            #Normalize direction
            #bullet.direction = bullet.direction.normalize()

            #Move bullet
            bullet.pos += bullet.direction * bullet.velocity
            bullet.rect.center = bullet.pos
            pygame.draw.rect(game.Game.screen,(255,0,0),bullet.rect)
            

              

            #game.Game.screen.blit(bullet.surf,bullet.rect)



            
        self.prune()


