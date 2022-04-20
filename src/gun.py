import pygame
import math
import game
import random

#Special Division because
def special_division(f,s):
  return f/s if s else 0

#Used to get the distance between the target, and bullets for the homing bullets
def distance_calculate(x1,y1,x2,y2):
  return math.sqrt(pow(x2-x1,2)+pow(y2-y1,2))

#Main Bullet Creation Class
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

#Main Gun Container Class
class Gun(pygame.sprite.Sprite):
    def __init__(self):
        self.isShooting = False
        self.bullets = []
        self.idCount = 0
        super().__init__()

    #Creates a bullet and then finds the distance vectors it must travel using pygame.math Vectors
    def create(self,initialpos,endpos,homing=False,bounce=False,pierce=False):
        
        pos = pygame.math.Vector2(initialpos)
        arctangent = math.atan2(endpos[1]-initialpos[1],endpos[0]-initialpos[0])
        dx = math.cos(arctangent)
        dy = math.sin(arctangent)
        direction = pygame.math.Vector2(dx,dy).normalize()
        #Used to add small amounts of spread to the bullets being fires
        direction[0] += random.uniform(-0.15,0.15)
        direction[1] += random.uniform(-0.15,0.15)
        direction = direction.normalize()
        #Pygame Surfaces and Rects
        surf = pygame.Surface((5,5))
        surf.fill((0,0,0))
        rect = surf.get_rect(
          center = initialpos
        )

        #Creating a new bullet from the above variables
        bullet = Bullet(self.idCount,pos,rect,direction,homing=True,bounce=bounce,pierce=pierce)

        #Add the bullet to the individual's gun class
        self.bullets.append(bullet)

        self.idCount += 1

      
    #Removes bullet from the gun
    def delete(self,bullet):
      for index in range(len(self.bullets)):
        if self.bullets[index].id == bullet.id:
          del self.bullets[index]
          break

    #Decides if the gun should be shooting at the current time
    def shooting(self,events=[]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.isShooting = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.isShooting = False

    #Deletes all bullets that have exited the screen boundries; Doesn't work if the bullet has the boundy attribute
    def prune(self):
        #Gets rid of all bullets not on screen
        for bullet in self.bullets:
          if not bullet.bounce:
            if bullet.rect.top <= 0 or bullet.rect.bottom >= game.Game.BOARD_HEIGHT or bullet.rect.left <= 0 or bullet.rect.right >= game.Game.BOARD_WIDTH:
                self.delete(bullet)
              
    #Cleans all bullets off of the screen for next round
    def clear(self):
      self.bullets.clear()
        

    def update(self):
        #Moves position along X axis
        for bullet in self.bullets:

          #Homing Bullets WIP
          if bullet.homing:
            #Homing Missle/Bullet Shinangians
            #Find closest enemy to bullets current position

            #Closest enemy to bullet is decides as the target
            target = None
            closest = 99999
            
            for instance in game.Game.WaveHandler.currentEnemies:
              EnemyX = instance.rect.x
              EnemyY = instance.rect.y
              dist = distance_calculate(EnemyX,EnemyY,bullet.rect.x,bullet.rect.y)
              if dist < closest:
                closest = dist
                target = instance
            
            #If there is a target, then slowely turn the bullet direction towards the target
            if target:
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
            
          #If the bullet hits the side of the screen, then bound off of the wall in the opposite direction. Immune to dying from leaving the screen
          if bullet.bounce:
            if bullet.rect.left < 0 or bullet.rect.right > game.Game.BOARD_WIDTH:
              bullet.direction[0] = -bullet.direction[0]
            if bullet.rect.top < 0 or bullet.rect.bottom > game.Game.BOARD_HEIGHT:
              bullet.direction[1] = -bullet.direction[1]


          #Move the bullet along the path of travel; Universal to all current type of bullets   
          bullet.pos += bullet.direction * bullet.speed
          bullet.rect.center = bullet.pos
          pygame.draw.rect(game.Game.screen,(255,0,0),bullet.rect)

        #Remove all bullets that have left the screen
        self.prune()


