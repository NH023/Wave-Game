import pygame
import math
import game



def special_division(f,s):
  return f/s if s else 0

def distance(x1,y1,x2,y2):
  return math.sqrt(pow(x2-x1,2)+pow(y2-y1,2))

class Bullet():
  def __init__(self,id,surf,rect,type,initialpos=None,endpos=None,dx=None,dy=None,velocity=None,target=None):
    self.id = id
    self.surf = surf
    self.rect = rect
    self.type = type
    self.initialpos = initialpos
    self.endpos = endpos
    self.dx =dx
    self.dy = dy
    self.velocity = velocity
    self.target = target
  def get_self(self):
    return self

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
        dx = self.speed*math.cos(arctangent)
        dy = self.speed*math.sin(arctangent)
        
        bullet = Bullet(self.idCount,surf,rect,"standard",initialpos,endpos,dx,dy)

        self.bullets.append(bullet)
        self.idCount += 1

    def createHoming(self,initialpos,_target):
      surf = pygame.Surface((5,5))
      surf.fill((0,0,0))
      rect = surf.get_rect(
        center = initialpos
      ) 

      bullet = Bullet(self.idCount,surf,rect,"homing",initialpos,target=_target)
      
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
            bullet.type.move_ip(bullet.dx,bullet.dy)                 
            game.Game.screen.blit(bullet.surf,bullet.rect)
          elif bullet.type == "homing":
            #Homing Missle/Bullet Shinangians
            #Find closest enemy to bullets current position
            target = 0
            closest = 100000000
            bulletpos = (bullet.rect.x,bullet.rect.y)
            for instance in game.Game.WaveHandler.currentEnemies:
              EnemyX = instance.rect.x
              EnemyY = instance.rect.y
              dist = distance(EnemyX,EnemyY,bulletpos[0],bulletpos[1])
              if dist < closest:
                closest = dist
                target = instance

            targetpos = (target.rect.x,target.rect.y)
            


            
            
            
            

            game.Game.screen.blit(bullet.surf,bullet.rect)
            
        self.prune()


