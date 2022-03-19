from game import Game

BOARD_WIDTH = 800
BOARD_HEIGHT = 600
caption = "Sick Game"

if __name__ == "__main__":
    game = Game(BOARD_WIDTH,BOARD_HEIGHT,caption)
    game.run()