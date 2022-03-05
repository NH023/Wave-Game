import pygame
from player import Player
from enemy import Basic, Speeder, Blaster
from board import Board
import time
pygame.init()



BOARD_HEIGHT = 600
BOARD_WIDTH = 800
BACKGROUND_COLOR = (255,255,255)

screen = Board(BOARD_WIDTH,BOARD_HEIGHT,"Super Awesome Game").screen

clock = pygame.time.Clock()
running = True

player = Player((BOARD_WIDTH/2,BOARD_HEIGHT/2))
current_enemies = [Basic((20,20)),Speeder((70,70)),Blaster((120,120))]
gunCooldown = 0.5
lastBulletFire = time.time()

def increaseing():
  for i in current_enemies:
    if i.type == 'speeder':
      i.increaseSpeed()

def blastershooting():
  for i in current_enemies:
    if i.type == 'blaster':
      i.shoot()

increment_time = time.time()
blaster_time = time.time()

while running:
    events = pygame.event.get()
    pressed_keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    player.move(pressed_keys)
    if pressed_keys[pygame.K_k]:
      for i in current_enemies:
        i.update()
    if pressed_keys[pygame.K_e]:
      print([i["rect"] for i in player.gun.bullets])


    screen.fill(BACKGROUND_COLOR)
    screen.blit(player.surf, player.rect)

    for enemy in current_enemies:
      if enemy.isAlive:
        screen.blit(enemy.surf, enemy.rect)
      else:
        current_enemies.remove(enemy)
      enemy.update()

    player.gun.shooting(events)


    if player.gun.isShooting:
      if lastBulletFire+gunCooldown < time.time():
        lastBulletFire = time.time()
        player.gun.create((player.rect.centerx,player.rect.centery),pygame.mouse.get_pos())

    player.gun.update()

    #Flip Display
    pygame.display.flip()
    
    clock.tick(7)

pygame.quit()
