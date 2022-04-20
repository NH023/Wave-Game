import pygame
import time
import game
from gun import Gun

#Main Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        #Pygame
        self.surf = pygame.Surface((25,25))
        self.surf.fill((0,0,0))
        Player.rect = self.surf.get_rect(
            center=pos
        )
        
        self.speed = 10
        #Player's gun instance
        Player.gun = Gun()
        #Cooldowns for gun
        self.last_shot = time.time()
        self.gunCooldown = 0
        #Alive
        self.isAlive = True

    #Player moves bases on the WASD or Arrow Keys
    def move(self,pressed_keys):
        #Move Up
        if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0,-self.speed)
        #Move Down
        if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0,self.speed)
        #Move Left
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed,0)
        #Move Right
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed,0)

        #Collision with the walls
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= game.Game.BOARD_HEIGHT:
            self.rect.bottom = game.Game.BOARD_HEIGHT
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= game.Game.BOARD_WIDTH:
            self.rect.right = game.Game.BOARD_WIDTH

    #Updates every frame
    def update(self,pressed_keys,events):
        self.move(pressed_keys)
        #Check to see if the player is holding down the fire key, if so set to true
        self.gun.shooting(events)
        if self.gun.isShooting:
            #If the last fire cooldown has expired then another bullet is created and fired
            if self.last_shot+self.gunCooldown < time.time():
                self.last_shot = time.time()
                self.gun.create(self.rect.center,pygame.mouse.get_pos(),bounce=True)
        #Update all bullets from this gun instance
        self.gun.update()
        game.Game.screen.blit(self.surf, self.rect)

    #Kills player when run by removeing from all groups and closing the game
    def doom(self):
        self.kill()
        self.isAlive = False

        
