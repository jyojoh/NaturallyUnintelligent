import random
import sys
import os

player_symbol = "X"

def take_turn():
    if os.path.exists("move_file"):
        opponent_move = open("move_file")
        if os.path.getsize("move_file") != 0:
            player_symbol = "O"

def minimax():
    return


if __name__ == '__main__':
    while not os.path.exists("end_game"):
        if os.path.exists("NaturallyUnintelligent.go"):
            f = open("NaturallyUnintelligent.go")
            take_turn()
    exit()