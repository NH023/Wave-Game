from enemy import Basic, Speeder, Blaster
from player import Player
import os
import game
import pygame
import time

#Wave Handler for handling waves (crazy how that works huh)
class WaveHandler():
    def __init__(self):
        self.currentRound = 0
        #Enemies present in the current wave
        self.currentEnemies = []
      
        #All waves are loaded from the ./waves folder in the same directory. All waves are contained in this variable. See ./waves/TEMPLATE.txt for how the wave text files work
        self.waves = []
      
        #If playground is set to true, then waves wont load, and the game loads to a blank arena with no enemies
        self.playground = False
        #Load the waves from folder of txts
        wavefiles = filter(lambda x: x != "TEMPLATE.txt", os.listdir("src/waves"))
        for wavefile in wavefiles:
            with open("src/waves/"+wavefile, "r") as f:
                print(wavefile)
                #Add wave to self.waves variable
                self.waves.append(f.read().split('\n'))
        
        #Font for wave counter in top left corner of screen
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        #Font for splashscreen between each round start
        self.splashfont = pygame.font.Font('freesansbold.ttf', 60)

    #When run, the next round is loaded from the self.waves variable
    def nextRound(self):
        if self.playground:
          return
        print("Current Round: " + str(self.currentRound + 1))
        #Gets the next round
        newWave = self.waves[self.currentRound]
        newEnemies = []

        #Clears bullets from players off of the screen
        Player.gun.clear()
        self.splash()
      
        for line in range(len(newWave)):
            #Skip comment lines in wave text files
            if newWave[line].startswith("#"):
              continue
            #Sets player position in wave text file
            if newWave[line].startswith("P"):
              code, x, y = newWave[line].split(' ')
              Player.rect.x = float(x) * game.Game.BOARD_WIDTH
              Player.rect.y = float(y) * game.Game.BOARD_HEIGHT
              continue
            #Gets the enemy type, and position of he enemy from the file
            eType, xPos,yPos = newWave[line].split(' ')
            xPos = float(xPos)
            yPos = float(yPos)

            xPos = game.Game.BOARD_WIDTH * xPos
            yPos = game.Game.BOARD_HEIGHT * yPos

            #Basic Type Enemy Creator
            if eType == 'B':
                newEnemies.append(Basic((xPos,yPos)))  
            #Speed Type Enemy Creator
            elif eType == 's':
                newEnemies.append(Speeder((xPos,yPos)))
            #Blaster Type Enemy Creator
            elif eType == 'b':
                newEnemies.append(Blaster((xPos,yPos)))

        self.currentEnemies = newEnemies
        self.currentRound += 1

    #Continues rendering the current round to the top left corner of the screen
    def counter(self):
        text = self.font.render(f"Wave {self.currentRound}",True,"black")
        textRect = text.get_rect()
        textRect.top = 0
        textRect.left = 0
        game.Game.screen.blit(text,textRect)
        
    #Renders the splash screen between each round
    def splash(self):
        game.Game.screen.fill((255,255,255))
        text = self.splashfont.render(f"Wave {self.currentRound+1}",True,"red")
        textRect = text.get_rect()
        textRect.center = (game.Game.BOARD_WIDTH/2, game.Game.BOARD_HEIGHT/2)
        game.Game.screen.blit(text,textRect)
        pygame.display.update()
        time.sleep(2)
      
    #Checks to see if the round should be advanced or if the game should end
    def check(self):
        self.counter()
        #No enemies left on screen, start next round from variables
        if len(self.currentEnemies) < 1:
            #If there are no more waves left then end the game
            if self.currentRound+1 > len(self.waves):
                print("GG Congrats, You Won")
                #Returns False to tell the game class to exit the game window
                return False
            #Start next round
            self.nextRound()
        #When True: Disallows the game class to exit the game
        return True
