import random
import sys
import os

player_symbol = "O"
time_limit = 10
turn_num = 0
moves_taken = []
board_state = []
opponent_move = ""

def take_turn():
    if os.path.exists("move_file"):
        with open("move_file") as f:
            opponent_move = f.readline()
        if os.path.getsize("move_file") == 0 and turn_num == 0:
            player_symbol = "X"
    next_board = parse_move(opponent_move) % 9
    next_moves = valid_moves(next_board)


def coord_convert(i, j):
    return (i * 9) + j

def parse_move(str):
    move = str.split()
    symbol = move[0]
    sub_board = move[1]
    board_coord = move[2]
    index = coord_convert(sub_board, board_coord)
    update_board(symbol, index)
    return index

def update_board(symbol, index):
    board_state[index] = symbol

def min(moveset):
    max(moveset)

def max(moveset):
    return

def pruning():
    return

def valid_moves(next_board):
    moveset = []
    subboard_state = board_state[next_board * 9 : next_board * 9 + 9]
    for index, tile in enumerate(subboard_state):
        if tile == "EMPTY":
            moveset.append(index + (next_board * 9))

    if moveset == []:
        for index, tile in enumerate(board_state):
            if tile == "EMPTY":
                moveset.append(index)
    return moveset


if __name__ == '__main__':
    board_state = ["EMPTY" for x in range(81)]

    while not os.path.exists("end_game"):
        if(len(moves_taken) == 0):
            with open("first_four_moves", "r") as f:
                moves_taken = f.readlines()
        if os.path.exists("NaturallyUnintelligent.go"):
            take_turn()
            turn_num += 1
    exit()
