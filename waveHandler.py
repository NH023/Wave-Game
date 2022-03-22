from enemy import Basic, Speeder, Blaster
import os
import game

class waveHandler():
    def __init__(self):
        self.currentRound = 0
        self.currentEnemies = []
        self.waves = []
        #Load the waves from the file
        wavefiles = filter(lambda x: x != "TEMPLATE.txt", os.listdir("waves"))
        for wavefile in wavefiles:
            with open("waves/"+wavefile, "r") as f:
                print(wavefile)
                self.waves.append(f.read().split('\n'))


    def nextRound(self):
        print("Current Round: " + str(self.currentRound + 1))
        newWave = self.waves[self.currentRound]
        newEnemies = []

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

        
    
    def check(self):
        if len(self.currentEnemies) < 1:
            if self.currentRound+1 > len(self.waves):
                print("GG Congrats, You Won")
                return False
            self.nextRound()
        return True