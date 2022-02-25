import pygame
class Board():
  def __init__(self,BOARD_WIDTH,BOARD_HEIGHT,caption):
    Board.BOARD_WIDTH = BOARD_WIDTH
    Board.BOARD_HEIGHT = BOARD_HEIGHT
    Board.screen = pygame.display.set_mode((BOARD_WIDTH,BOARD_HEIGHT))
    Board.caption = pygame.display.set_caption(caption)
  


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