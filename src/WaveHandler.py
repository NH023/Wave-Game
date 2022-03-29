from enemy import Basic, Speeder, Blaster
from player import Player
import os
import game
import pygame
import time

class WaveHandler():
    def __init__(self):
        self.currentRound = 0
        self.currentEnemies = []
        self.waves = []
        #Load the waves from the file
        wavefiles = filter(lambda x: x != "TEMPLATE.txt", os.listdir("src/waves"))
        for wavefile in wavefiles:
            with open("src/waves/"+wavefile, "r") as f:
                print(wavefile)
                self.waves.append(f.read().split('\n'))
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.splashfont = pygame.font.Font('freesansbold.ttf', 60)


    def nextRound(self):
        print("Current Round: " + str(self.currentRound + 1))
        newWave = self.waves[self.currentRound]
        newEnemies = []

        for bullet in Player.gun.bullets:
            Player.gun.delete(bullet)

        self.splash()
      
        for enemy in newWave:
            eType, xPos,yPos = enemy.split(' ')
            xPos = float(xPos)
            yPos = float(yPos)

            xPos = game.Game.BOARD_WIDTH * xPos
            yPos = game.Game.BOARD_HEIGHT * yPos

            if eType == 'B':
                newEnemies.append(Basic((xPos,yPos)))  
            elif eType == 's':
                newEnemies.append(Speeder((xPos,yPos)))
            elif eType == 'b':
                newEnemies.append(Blaster((xPos,yPos)))

        self.currentEnemies = newEnemies

        self.currentRound += 1

    def counter(self):
        text = self.font.render(f"Wave {self.currentRound}",True,"black")
        textRect = text.get_rect()
        textRect.top = 0
        textRect.left = 0
        game.Game.screen.blit(text,textRect)
        
      
    def splash(self):
        game.Game.screen.fill((255,255,255))
        text = self.splashfont.render(f"Wave {self.currentRound+1}",True,"red")
        textRect = text.get_rect()
        textRect.center = (game.Game.BOARD_WIDTH/2, game.Game.BOARD_HEIGHT/2)
        game.Game.screen.blit(text,textRect)
        pygame.display.update()
        time.sleep(2)
      
      
    def check(self):
        self.counter()
        if len(self.currentEnemies) < 1:
            if self.currentRound+1 > len(self.waves):
                print("GG Congrats, You Won")
                return False
            self.nextRound()
        return True
