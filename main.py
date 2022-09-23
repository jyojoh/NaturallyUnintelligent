import random
import sys
import os

player_symbol = "X"
time_limit = 10
moves_taken = []

def take_turn():
    if os.path.exists("move_file"):
        opponent_move = open("move_file")
        if os.path.getsize("move_file") != 0:
            player_symbol = "O"

def minimax():
    return

def valid_moves():
    return


if __name__ == '__main__':
    while not os.path.exists("end_game"):
        if(len(moves_taken) == 0):
            with open("first_four_moves", "r") as f:
                moves_taken = f.readlines()
        if os.path.exists("NaturallyUnintelligent.go"):
            take_turn()
    exit()