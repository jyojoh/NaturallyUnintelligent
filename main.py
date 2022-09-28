import random
import sys
import os

player_symbol = "O"
time_limit = 10
turn_num = 0
moves_taken = []
board_state = []
opponent_move = ""
boards_won = []

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
    sub_board = move[1] #Sub-Board number, from 0-8
    board_coord = move[2] #Sub-board coordinate, from 0-8
    index = coord_convert(sub_board, board_coord)
    update_board(symbol, index)
    return index

def update_board(symbol, index):
    board_state[index] = symbol
    check_win(index // 9)

def check_win(sub_board):
    if boards_won[sub_board] != "None":
        return

    center_index = sub_board * 9 + 4

    if board_state[center_index -1] == board_state[center_index] and board_state[center_index +1] == board_state[center_index] and board_state[center_index - 1] != "EMPTY": #Center row
        boards_won[sub_board] = board_state[center_index -1]
        fill_subboard(sub_board)
        return True
    elif board_state[center_index +2] == board_state[center_index+3] and board_state[center_index +4] == board_state[center_index+3] and board_state[center_index +2] != "EMPTY": #Bottom row
        boards_won[sub_board] = board_state[center_index +2]
        fill_subboard(sub_board)
        return True
    elif board_state[center_index -4] == board_state[center_index-3] and board_state[center_index -2] == board_state[center_index-3] and board_state[center_index - 4] != "EMPTY": #Top row
        boards_won[sub_board] = board_state[center_index -4]
        fill_subboard(sub_board)
        return True
    elif board_state[center_index -4] == board_state[center_index-1] and board_state[center_index -4] == board_state[center_index+2] and board_state[center_index - 4] != "EMPTY": #First column
        boards_won[sub_board] = board_state[center_index - 4]
        fill_subboard(sub_board)
        return True
    elif board_state[center_index -3] == board_state[center_index-1] and board_state[center_index -3] == board_state[center_index+3] and board_state[center_index - 3] != "EMPTY": #Second column
        boards_won[sub_board] = board_state[center_index -3]
        fill_subboard(sub_board)
        return True
    elif board_state[center_index -2] == board_state[center_index+1] and board_state[center_index -2] == board_state[center_index+4] and board_state[center_index - 2] != "EMPTY": #Third column
        boards_won[sub_board] = board_state[center_index -2]
        fill_subboard(sub_board)
        return True
    elif board_state[center_index -4] == board_state[center_index] and board_state[center_index] == board_state[center_index+4] and board_state[center_index] != "EMPTY": #Top Left Bottom Right Diag
        boards_won[sub_board] = board_state[center_index -4]
        fill_subboard(sub_board)
        return True
    elif board_state[center_index -2] == board_state[center_index] and board_state[center_index] == board_state[center_index+2] and board_state[center_index] != "EMPTY": #Top Right Bottom Left Diag
        boards_won[sub_board] = board_state[center_index -2]
        fill_subboard(sub_board)
        return True

    return False

def fill_subboard(sub_board):
    for tile in board_state[sub_board * 9 : sub_board * 9 + 9]:
        tile = boards_won[sub_board]

def min(moveset):
    max(moveset)

def max(moveset):
    return

def pruning():
    return

def valid_moves(next_board):
    moveset = []

    if boards_won[next_board] != "None":
        for index, tile in enumerate(board_state):
            if tile == "EMPTY":
                moveset.append(index)
        return moveset

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
    boards_won = ["None" for x in range(9)]
    while not os.path.exists("end_game"):
        if(len(moves_taken) == 0):
            with open("first_four_moves", "r") as f:
                moves_taken = f.readlines()
        if os.path.exists("NaturallyUnintelligent.go"):
            take_turn()
            turn_num += 1
    exit()
