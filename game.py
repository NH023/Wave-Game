import pygame
from player import Player
from enemy import Enemy, Basic, Speeder, Blaster

class Game():
  def __init__(self,BOARD_WIDTH,BOARD_HEIGHT,caption):
    Game.BOARD_WIDTH = BOARD_WIDTH
    Game.BOARD_HEIGHT = BOARD_HEIGHT
    Game.screen = pygame.display.set_mode((BOARD_WIDTH,BOARD_HEIGHT))
    Game.caption = pygame.display.set_caption(caption)
    Game.player = Player((Game.BOARD_WIDTH/2,Game.BOARD_HEIGHT/2))
  

  #Get the object that needs to be checked for damage, if its the player, then get all enemies and enemy bullets, if any collide with the player, then damage the player. If its the enemy, get all player bullets and check if any collide with the enemy, if so, damage the enemy.
  def check_damage(self):
    for enemy in Enemy.instances:
      if Game.player.rect.colliderect(enemy.rect):
        Game.player.doom()
      #Check if enemy has a gun, if so check if any bullets collide with the player
      if enemy.type == "blaster":
        for bullet in enemy.gun.bullets:
          if Player.rect.colliderect(bullet["rect"]):
            Game.player.doom()
            enemy.gun.remove(bullet)
    for enemy in Enemy.instances:
      for bullet in Game.player.gun.bullets:
        if enemy.rect.colliderect(bullet["rect"]):
          enemy.damage()
          Player.gun.remove(bullet)

  def run(self):
    #Setup
    running = True
    clock = pygame.time.Clock()

    #Create enemies
    current_enemies = [Basic((20,20)),Speeder((70,70)),Blaster((120,120))]


    #Main Loop
    while running:
      events = pygame.event.get()
      pressed_keys = pygame.key.get_pressed()

      #Check for events
      for event in events:
        if event.type == pygame.QUIT:
          running = False

      #Check for damage
      self.check_damage()

      #Draw
      Game.screen.fill((255,255,255))


      #Update player
      if Game.player.isAlive:
        Game.player.update(pressed_keys,events)
      else:
        running = False

      #Update enemies
      for enemy in current_enemies:
        if enemy.isAlive:
          enemy.update()
        else:
          current_enemies.remove(enemy)


      #Flip Display
      pygame.display.flip()
      #Update Clock
      clock.tick(30)



  #Can be worked around later


  # def boundDetection(self,rect):
  #   if self.rect.top <= 0:
  #       self.rect.top = 0
  #   if self.rect.bottom >= self.BOARD_HEIGHT:
  #       self.rect.bottom = self.BOARD_HEIGHT
  #   if self.rect.left <= 0:
  #       self.rect.left = 0
  #   if self.rect.right >= self.BOARD_WIDTH:
  #       self.rect.right = self.BOARD_WIDTH