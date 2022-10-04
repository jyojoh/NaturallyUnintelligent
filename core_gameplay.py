import random

import numpy as np

#  Constants
#  Player markers must be greater than NO_MARKER
#  DRAW most be less than NO_MARKER
DRAW = -1
NO_MARKER = 0
PLAYER0_MARKER = 1
PLAYER1_MARKER = 2
NO_LOCAL_BOARD = -1

MARKERS = [PLAYER0_MARKER, PLAYER1_MARKER]

BAD_MOVE_I_WIN = -2
BAD_MOVE_I_LOST = -3
BAD_MOVE_DRAW = -4

WIN_INDEXES = [[0, 1, 2],
               [3, 4, 5],
               [6, 7, 8],
               [0, 4, 8],
               [6, 4, 2],
               [0, 3, 6],
               [1, 4, 7],
               [2, 5, 8]]


# Effectively functional
# Returns the winner marker of the board
def check_3x3_win(board):
    for indexes in WIN_INDEXES:
        if board[indexes[0]] == board[indexes[1]] and \
                board[indexes[1]] == board[indexes[2]] and \
                board[indexes[0]] != NO_MARKER:
            return board[indexes[0]]

    # If no one has won but the board is full, is draw
    if NO_MARKER not in board:
        return DRAW
    return NO_MARKER


# The local board numbers are
# 0 1 2
# 3 4 5
# 6 7 8
#
# The global numbers are of the form
# 0 1 2 | 09 10 11 |
# 3 4 5 | 12 13 14 |
# 6 7 8 | 15 16 17 |


# FUNCTIONAL
# Converts a global square number (0-80) to a local
# pair containing [local_square_number, board_number]
def global_to_local(g):
    lb_num = int(np.floor(g / 9))
    l = g - lb_num * 9
    return [l, lb_num]


# FUNCTIONAL
# Converts a local pair containing [local_square_number, board_number]
# to a global location 0-80
def local_to_global(l):
    return l[0] + 9 * l[1]


# Gets the valid moves based on the global board state and
# the currently active board
def valid_moves(big_board, current_local, can_move_in_won_board):
    moves = []
    if current_local == NO_LOCAL_BOARD:
        for i in range(0, 9):
            moves = moves + valid_moves_3x3_global(big_board[i], i, can_move_in_won_board)
    else:
        moves = valid_moves_3x3_global(big_board[current_local], current_local, can_move_in_won_board)
    return moves


# Returns the valid moves of a 3x3 board converted to global numbers
def valid_moves_3x3_global(board, board_number, can_move_in_won_board):
    l_moves = valid_moves_3x3(board, can_move_in_won_board)
    moves = []
    for move in l_moves:
        moves.append(local_to_global([move, board_number]))
    return moves


# Returns the playable moves on a basic 3x3 board
def valid_moves_3x3(board, can_move_in_won_board):
    moves = []

    # There are no valid moves on a won board
    if not can_move_in_won_board:
        if check_3x3_win(board):
            return moves

    for i in range(0, 9):
        val = board[i]
        if val == NO_MARKER:
            moves.append(i)
    return moves


# Mutates big_board
# Marks a big board at the global location given
def mark_big_board(big_board, g_sq, marker):
    local = global_to_local(g_sq)
    big_board[local[1], local[0]] = marker


# Mutates big_board, main_board_wins
# Marks a big board at the global location given
# Returns the number of the local board that was won if one was won, -1 otherwise
def handle_mark_big_board(big_board, g_sq, marker, main_board_wins):
    mark_big_board(big_board, g_sq, marker)
    local_board_number = global_to_local(g_sq)[1]
    local_winner = check_3x3_win(big_board[local_board_number])
    if local_winner != NO_MARKER:
        # If there was a local victory, see then if that ended the game
        main_board_wins[local_board_number] = local_winner
        return local_board_number
    return -1

def get_init_random_string():
    okay = False
    nums = []
    while not okay:
        nums = generate_valid_random_string()
        print(nums)
        if not(nums[0] == 4 and nums[1] == 4 and nums[3] == 4 and nums[2] != 4 and nums[4] != 4):
            okay = True
    return nums


def generate_valid_random_string():
    banned = []
    for i in range(9):
        banned.append(set())

    nums = []
    for i in range(5):
        valid = set(range(9))
        if i > 0:
            valid = valid - banned[nums[i - 1]]
        choice = random.choice(list(valid))
        nums.append(choice)
        if i > 0:
            banned[nums[i-1]].add(choice)

    return nums

