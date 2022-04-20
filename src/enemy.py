import pygame
import time
from player import Player
from gun import Gun
import game

#Special division because divide by zero error is big dumb
def special_division(f,s):
  return f/s if s else 0

#Main Enemy Parent Class
class Enemy(pygame.sprite.Sprite):
  def __init__(self, size, color, pos):
    super().__init__()
    #Pygame
    self.surf = pygame.Surface(size)
    self.surf.fill(color)
    self.rect = self.surf.get_rect(
      center=pos
    )
    #Alive
    self.isAlive = True

  #If enemy health falls below 0 then they are removed from all groups, and removed from the game
  def checkIfDead(self):
    if self.health <= 0:
      self.kill()
      self.isAlive = False

  #Damages the enemy instance
  def damage(self):
    self.health -= 1
    self.checkIfDead()
      


#Basic Enemy;
  #Movement: Moves in a line towards the Player
  #Damage: Body damages Player
class Basic(Enemy):
  def __init__(self,pos):
    #Basic Enemy Variables
    self.type = "basic"
    self.speed = 2
    self.size = (20,20)
    self.color = (255,0,0)
    self.health = 2
    super().__init__(self.size,self.color,pos)

  def move(self):
    playerpos = (Player.rect.centerx,Player.rect.centery)
    enemypos = (self.rect.centerx,self.rect.centery)
    #Calculates the X and Y Difference for where it needs to go to meet the player
    x_move = special_division((playerpos[0] - enemypos[0]),abs(playerpos[0] - enemypos[0])) * self.speed
    if x_move > playerpos[0]:
      x_move = playerpos[0]
    y_move = special_division((playerpos[1] - enemypos[1]),abs(playerpos[1] - enemypos[1])) * self.speed
    if y_move > playerpos[1]:
      y_move = playerpos[1]
    
    self.rect.move_ip(x_move,y_move)
    
    #Collision
    if self.rect.top <= 0:
        self.rect.top = 0
    if self.rect.bottom >= game.Game.BOARD_HEIGHT:
        self.rect.bottom = game.Game.BOARD_HEIGHT
    if self.rect.left <= 0:
        self.rect.left = 0
    if self.rect.right >= game.Game.BOARD_WIDTH:
        self.rect.right = game.Game.BOARD_WIDTH

  def update(self):
    #Moves toward player
    self.move()
    game.Game.screen.blit(self.surf, self.rect)


#Speed Enemy
  #Movement: Moves straight towards player, but increases speed over time
  #Damage: Body damages Player
class Speeder(Enemy):
  #Increases Speed Over Time
  def __init__(self,pos):
    #Speeder Enemy Variables
    self.type = "speeder"
    self.size = (15,15)
    self.color = (100,175,175)
    self.health = 2
    #Starting Speed
    self.speed = 1
    #How much each increment should be
    self.increment = 1
    #How much time should pass between each speed increase
    self.cooldown=1 #Seconds
    self.incrementTime = time.time()
    super().__init__(self.size,self.color,pos)
    
    
  def move(self):
    playerpos = (Player.rect.centerx,Player.rect.centery)
    enemypos = (self.rect.centerx,self.rect.centery)

    #Calculates the X and Y Difference for where it needs to go to meet the player
    x_move = special_division((playerpos[0] - enemypos[0]),abs(playerpos[0] - enemypos[0])) * self.speed
    if x_move > playerpos[0]:
      x_move = playerpos[0]
    y_move = special_division((playerpos[1] - enemypos[1]),abs(playerpos[1] - enemypos[1])) * self.speed
    if y_move > playerpos[1]:
      y_move = playerpos[1]
    
    self.rect.move_ip(x_move,y_move)

    #Collision detection
    if self.rect.top <= 0:
        self.rect.top = 0
    if self.rect.bottom >= game.Game.BOARD_HEIGHT:
        self.rect.bottom = game.Game.BOARD_HEIGHT
    if self.rect.left <= 0:
        self.rect.left = 0
    if self.rect.right >= game.Game.BOARD_WIDTH:
        self.rect.right = game.Game.BOARD_WIDTH
      
  #Increases Enemy Speed
  def increaseSpeed(self):
    self.speed += self.increment

  def update(self):
    self.move()
    #Increases speed once the cooldown timer has expired
    if self.incrementTime+self.cooldown < time.time():
      self.speed += self.increment
      self.incrementTime = time.time()
    game.Game.screen.blit(self.surf, self.rect)

    
#Blaster Enemy
  #Movement: Nonexistint; Stands still
  #Damage: Shoots bullets at Player to deal damage
class Blaster(Enemy):
  #Shoots Bullets
  def __init__(self,pos):
    #Blaster Enemy Variables
    self.type = "blaster"
    self.size = (15,15)
    self.color = (175,4,175)
    self.health = 1
    self.speed = 1
    self.blasterTime = time.time()
    #Time between each new bullet
    self.cooldown = 1
    #Enemy gun instance
    self.gun = Gun()
    super().__init__(self.size,self.color,pos)
  
  #Creates bullet to be shot
  def shoot(self):
    self.gun.create((self.rect.centerx,self.rect.centery),(Player.rect.centerx,Player.rect.centery))


  def update(self):
    #Once the cooldown is expried a new bullet is created to be shot at the player
    if self.blasterTime+self.cooldown < time.time():
      self.shoot()
      self.blasterTime = time.time()
    self.gun.update()
    #Append to screen
    game.Game.screen.blit(self.surf, self.rect)
    