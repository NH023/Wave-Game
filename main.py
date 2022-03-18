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




while running:
    events = pygame.event.get()
    pressed_keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            running = False


    screen.fill(BACKGROUND_COLOR)
    screen.blit(player.surf, player.rect)

    for enemy in current_enemies:
      if enemy.isAlive:
        screen.blit(enemy.surf, enemy.rect)
      else:
        current_enemies.remove(enemy)
      enemy.update()

    player.update(pressed_keys,events)

    #Flip Display
    pygame.display.flip()
    
    clock.tick(30)

pygame.quit()
