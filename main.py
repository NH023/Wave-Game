import pygame
from player import Player
from enemy import Basic, Speeder
from board import Board
from gun import Gun
import time
pygame.init()



BOARD_HEIGHT = 350
BOARD_WIDTH = 400
BACKGROUND_COLOR = (255,255,255)

screen = Board(BOARD_WIDTH,BOARD_HEIGHT,"Super Awesome Game").screen

clock = pygame.time.Clock()
running = True

player = Player((BOARD_WIDTH/2,BOARD_HEIGHT/2))
current_enemies = [Basic((20,20)),Speeder((70,70))]
gunCooldown = 0.5
lastBulletFire = time.time()
gun = Gun()

def increaseing():
  for i in current_enemies:
    if i.type == 'speeder':
      i.increaseSpeed()

time_start = time.time()

while running:
    events = pygame.event.get()
    pressed_keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    player.move(pressed_keys)
    if pressed_keys[pygame.K_k]:
      for i in current_enemies:
        i.doom()
    if pressed_keys[pygame.K_e]:
      print([i["rect"] for i in gun.bullets])


    screen.fill(BACKGROUND_COLOR)
    screen.blit(player.surf, player.rect)

    for enemy in current_enemies:
      if enemy.isAlive:
        screen.blit(enemy.surf, enemy.rect)
      else:
        current_enemies.remove(enemy)
      enemy.move()

    gun.shooting(events)


    if gun.isShooting:
      if lastBulletFire+gunCooldown < time.time():
        lastBulletFire = time.time()
        gun.create()
    gun.prune()
    gun.update()

    #Flip Display
    pygame.display.flip()
    if time_start+1 < time.time():
      increaseing()
      time_start = time.time()
    clock.tick(30)

pygame.quit()
