from game import Game

BOARD_WIDTH = 600
BOARD_HEIGHT = 400
caption = "Spec Lork Mork Spork Typa Game"

if __name__ == "__main__":
    game = Game(BOARD_WIDTH,BOARD_HEIGHT,caption)
    game.run()