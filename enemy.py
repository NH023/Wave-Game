import pygame
import time
from board import Board
from player import Player
from gun import Gun

def special_division(f,s):
  return f/s if s else 0

class Enemy(pygame.sprite.Sprite,Board):
  instances = []
  def __init__(self, size, color, pos):
    super().__init__()
    self.__class__.instances.append(self)
    self.surf = pygame.Surface(size)
    self.surf.fill(color)
    self.rect = self.surf.get_rect(
      center=pos
    )
    self.isAlive = True
    self.checkables = ["move","shoot","pain"]
    
  def doom(self):
    self.kill()
    self.isAlive = False

  def pain(self):
    #Get all of the player bullets shot and if any collide with the enemy, then life is lost. That bullet then gets deleted.
    players_bullets = Player.gun.bullets
    for bullet in players_bullets:
      #if self.rect.left < bullet["rect"].centery < self.rect.right and self.rect.top < bullet["rect"].centerx < self.rect.bottom:
      if self.rect.colliderect(bullet['rect']):
        self.health -= 1
        print(self.health,self.type)
        Player.gun.remove(bullet)
        if self.health < 1:
          self.doom()



class Basic(Enemy):
  def __init__(self,pos):
    self.type = "basic"
    self.speed = 2
    self.size = (20,20)
    self.color = (255,0,0)
    self.health = 2
    super().__init__(self.size,self.color,pos)
    #super().__class__.instances.append(self)

  def move(self):
    playerpos = (Player.rect.centerx,Player.rect.centery)
    enemypos = (self.rect.centerx,self.rect.centery)

    x_move = special_division((playerpos[0] - enemypos[0]),abs(playerpos[0] - enemypos[0])) * self.speed
    if x_move > playerpos[0]:
      x_move = playerpos[0]
    y_move = special_division((playerpos[1] - enemypos[1]),abs(playerpos[1] - enemypos[1])) * self.speed
    if y_move > playerpos[1]:
      y_move = playerpos[1]
    
    self.rect.move_ip(x_move,y_move)
    
    if self.rect.top <= 0:
        self.rect.top = 0
    if self.rect.bottom >= self.BOARD_HEIGHT:
        self.rect.bottom = self.BOARD_HEIGHT
    if self.rect.left <= 0:
        self.rect.left = 0
    if self.rect.right >= self.BOARD_WIDTH:
        self.rect.right = self.BOARD_WIDTH
  def update(self):
    self.move()
    self.pain()

class Speeder(Enemy):
  #Increases Speed Over Time
  def __init__(self,pos):
    self.type = "speeder"
    self.size = (15,15)
    self.color = (100,175,175)
    self.speed = 1
    self.increment = 0.2
    self.health = 2
    super().__init__(self.size,self.color,pos)
    #super().__class__.instances.append(self)
    
    
  def move(self):
    playerpos = (Player.rect.centerx,Player.rect.centery)
    enemypos = (self.rect.centerx,self.rect.centery)

    x_move = special_division((playerpos[0] - enemypos[0]),abs(playerpos[0] - enemypos[0])) * self.speed
    if x_move > playerpos[0]:
      x_move = playerpos[0]
    y_move = special_division((playerpos[1] - enemypos[1]),abs(playerpos[1] - enemypos[1])) * self.speed
    if y_move > playerpos[1]:
      y_move = playerpos[1]
    
    self.rect.move_ip(x_move,y_move)
    
    if self.rect.top <= 0:
        self.rect.top = 0
    if self.rect.bottom >= self.BOARD_HEIGHT:
        self.rect.bottom = self.BOARD_HEIGHT
    if self.rect.left <= 0:
        self.rect.left = 0
    if self.rect.right >= self.BOARD_WIDTH:
        self.rect.right = self.BOARD_WIDTH
  def increaseSpeed(self):
    self.speed += self.increment

  def update(self):
    self.move()
    if self.incrementTime+1 < time.time():
      self.speed += self.increment
      self.incrementTime = time.time()
    self.pain()
    
  
class Blaster(Enemy):
  #Shoots Bullets
  def __init__(self,pos):
    self.type = "blaster"
    self.size = (15,15)
    self.color = (175,4,175)
    self.speed = 1
    self.blasterTime = time.time()
    self.health = 1
    self.gun = Gun()
    super().__init__(self.size,self.color,pos)
  
    
    
  def move(self):
    playerpos = (Player.rect.centerx,Player.rect.centery)
    enemypos = (self.rect.centerx,self.rect.centery)

    x_move = special_division((playerpos[0] - enemypos[0]),abs(playerpos[0] - enemypos[0])) * self.speed
    if x_move > playerpos[0]:
      x_move = playerpos[0]
    y_move = special_division((playerpos[1] - enemypos[1]),abs(playerpos[1] - enemypos[1])) * self.speed
    if y_move > playerpos[1]:
      y_move = playerpos[1]
    
    self.rect.move_ip(x_move,y_move)
    
    if self.rect.top <= 0:
        self.rect.top = 0
    if self.rect.bottom >= self.BOARD_HEIGHT:
        self.rect.bottom = self.BOARD_HEIGHT
    if self.rect.left <= 0:
        self.rect.left = 0
    if self.rect.right >= self.BOARD_WIDTH:
        self.rect.right = self.BOARD_WIDTH

    self.gun.update()
    
  def shoot(self):
    self.gun.create((self.rect.centerx,self.rect.centery),(Player.rect.centerx,Player.rect.centery))

  def update(self):
    if self.blasterTime+1 < time.time():
      self.shoot()
      self.blasterTime = time.time()
    self.pain()
    