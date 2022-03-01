import pygame
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
    
  def doom(self):
    self.kill()
    self.isAlive = False


class Basic(Enemy):
  def __init__(self,pos):
    self.type = "basic"
    self.speed = 2
    self.size = (20,20)
    self.color = (255,0,0)
    self.health = 10
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


class Speeder(Enemy):
  #Increases Speed Over Time
  def __init__(self,pos):
    self.type = "speeder"
    self.size = (15,15)
    self.color = (100,175,175)
    self.speed = 1
    self.increment = 0.2
    self.health = 10
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

  
class Blaster(Enemy):
  #Shoots Bullets
  def __init__(self,pos):
    self.type = "blaster"
    self.size = (15,15)
    self.color = (175,4,175)
    self.speed = 1
    self.increment = 0.2
    self.health = 10
    self.gun = Gun()
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

    self.gun.update()
    
  def shoot(self):
    self.gun.create((self.rect.centerx,self.rect.centery),(Player.rect.centerx,Player.rect.centery))
