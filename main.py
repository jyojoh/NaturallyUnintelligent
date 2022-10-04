import sys
import os
import time

player_symbol = "O"
opponent_symbol = "X"
time_limit = 10.0
moves_taken = []
board_state = []
boards_won = []
scoreArr = []


def take_turn():
    if os.path.exists("move_file"):
        with open("move_file") as f:
            opponent_move = f.readline()
        if os.path.getsize("move_file") == 0:
            opponent_move = moves_taken[3]
    next_board = parse_move(opponent_move) % 9
    print("Next board is " + str(next_board))
    next_moves = valid_moves(next_board)
    next_move = minimax(next_moves, True, 6, -sys.maxsize, sys.maxsize, next_moves[0], time.time())
    move_string = "NaturallyUnintelligent " + str(next_move // 9) + " " + str(next_move % 9)
    print(move_string)

    f = open("move_file", "r+")
    f.seek(0)
    f.write(move_string)
    f.truncate()
    f.close()

    update_board(player_symbol, next_move)


def coord_convert(i, j):
    i = int(i)
    j = int(j)
    return (i * 9) + j


def parse_move(str):
    move = str.split()
    symbol = opponent_symbol

    if move[0] == "NaturallyUnintelligent":
        symbol = player_symbol

    sub_board = int(move[1])  # Sub-Board number, from 0-8
    board_coord = int(move[2])  # Sub-board coordinate, from 0-8
    index = coord_convert(sub_board, board_coord)
    update_board(symbol, index)
    return index


def update_board(symbol, index):
    board_state[index] = symbol
    print("Placing " + symbol + " at " + "subboard " + str(index // 9) + " coord " + str(index % 9))
    check_win(index // 9, False)


def check_win(sub_board, eval):
    if boards_won[sub_board] != "None":
        return

    center_index = sub_board * 9 + 4

    if board_state[center_index - 1] == board_state[center_index] and board_state[center_index + 1] == board_state[center_index] and board_state[center_index - 1] != "EMPTY":  # Center row
        if not eval:
            boards_won[sub_board] = board_state[center_index - 1]
            fill_subboard(sub_board)
        return True
    elif board_state[center_index + 2] == board_state[center_index + 3] and board_state[center_index + 4] == board_state[center_index + 3] and board_state[center_index + 2] != "EMPTY":  # Bottom row
        if not eval:
            boards_won[sub_board] = board_state[center_index + 2]
            fill_subboard(sub_board)
        return True
    elif board_state[center_index - 4] == board_state[center_index - 3] and board_state[center_index - 2] == board_state[center_index - 3] and board_state[center_index - 4] != "EMPTY":  # Top row
        if not eval:
            boards_won[sub_board] = board_state[center_index - 4]
            fill_subboard(sub_board)
        return True
    elif board_state[center_index - 4] == board_state[center_index - 1] and board_state[center_index - 4] == board_state[center_index + 2] and board_state[center_index - 4] != "EMPTY":  # First column
        if not eval:
            boards_won[sub_board] = board_state[center_index - 4]
            fill_subboard(sub_board)
        return True
    elif board_state[center_index - 3] == board_state[center_index] and board_state[center_index] == board_state[center_index + 3] and board_state[center_index] != "EMPTY":  # Second column
        if not eval:
            boards_won[sub_board] = board_state[center_index - 3]
            fill_subboard(sub_board)
        return True
    elif board_state[center_index - 2] == board_state[center_index + 1] and board_state[center_index - 2] == board_state[center_index + 4] and board_state[center_index - 2] != "EMPTY":  # Third column
        if not eval:
            boards_won[sub_board] = board_state[center_index - 2]
            fill_subboard(sub_board)
        return True
    elif board_state[center_index - 4] == board_state[center_index] and board_state[center_index] == board_state[center_index + 4] and board_state[center_index] != "EMPTY":  # Top Left Bottom Right Diag
        if not eval:
            boards_won[sub_board] = board_state[center_index - 4]
            fill_subboard(sub_board)
        return True
    elif board_state[center_index - 2] == board_state[center_index] and board_state[center_index] == board_state[center_index + 2] and board_state[center_index] != "EMPTY":  # Top Right Bottom Left Diag
        if not eval:
            boards_won[sub_board] = board_state[center_index - 2]
            fill_subboard(sub_board)
        return True

    return False


def check_block(move):
    board_state[move] = opponent_symbol
    if check_win(move // 9, True):
        board_state[move] = "EMPTY"
        return True
    board_state[move] = "EMPTY"
    return False


def fill_subboard(sub_board):
    for idx in range(sub_board * 9, sub_board * 9 + 9):
        board_state[idx] = "Filled"
    print(str(sub_board) + " has been won.")


def minimax(moveset, isMax, depth, a, b, best_move, start_time):
    bMove = best_move
    currSymbol = opponent_symbol

    if time.time() - start_time >= time_limit - 0.1:
        print("No Time! Returning best move.")
        return bMove
    if depth == 0:
        return bMove

    if isMax:
        currSymbol = player_symbol
        for move in moveset:
            score = heuristic(move, currSymbol)
            if score > a:
                a = score
                bMove = move
            minimax(valid_moves(move % 9), not isMax, depth - 1, a, b, bMove, start_time)
            board_state[move] = "EMPTY"

            if a >= b:
                break

        return bMove

    else:
        currSymbol = opponent_symbol
        for idx, move in enumerate(moveset):
            score = -heuristic(move, currSymbol)
            if score < b:
                b = score
                bMove = move
            minimax(valid_moves(move % 9), not isMax, depth - 1, a, b, bMove, start_time)
            board_state[move] = "EMPTY"

            if a >= b:
                break
        return bMove


def heuristic(move, symbol):
    move_score = 0
    board_state[move] = symbol
    if check_win(move // 9, True):
        move_score += 5

    if check_block(move):
        move_score += 3

    if check_opponent_win(move):
        move_score -= 3
        if move // 9 == 4:
            move_score -= 1

    # If player wins on subsequent board in 1 move, don't send opponent to that board. This causes loss.
    if check_player_win(move):
        move_score -= 1
        if move // 9 == 4:
            move_score -= 1

    # Want to take center tile in sub-board. This ensures victory.
    if move % 9 == 4:
        move_score += 1
        if move // 9 == 4:
            move_score += 1

    return move_score


def check_player_win(move):
    sub_board = move // 9
    if boards_won[sub_board] != "None":
        return False
    check_moves = valid_moves(sub_board)

    for index in range(len(check_moves)):
        board_state[check_moves[index]] = player_symbol
        if check_win(sub_board, True):
            board_state[check_moves[index]] = "EMPTY"
            return True
        board_state[check_moves[index]] = "EMPTY"
    return False


def check_opponent_win(move):
    sub_board = move // 9
    if boards_won[sub_board] != "None":
        return False
    check_moves = valid_moves(sub_board)

    for index in range(len(check_moves)):
        board_state[check_moves[index]] = opponent_symbol
        if check_win(sub_board, True):
            board_state[check_moves[index]] = "EMPTY"
            return True
        board_state[check_moves[index]] = "EMPTY"
    return False


def valid_moves(next_board):
    moveset = []

    if boards_won[next_board] != "None":
        for index, tile in enumerate(board_state):
            if tile == "EMPTY":
                moveset.append(index)
        return moveset

    subboard_state = board_state[next_board * 9: next_board * 9 + 9]
    for index, tile in enumerate(subboard_state):
        if tile == "EMPTY":
            moveset.append(index + (next_board * 9))

    if moveset == []:
        for index, tile in enumerate(board_state):
            if tile == "EMPTY":
                moveset.append(index)

    return moveset


if __name__ == '__main__':
    canPlay = True
    board_state = ["EMPTY" for x in range(81)]
    boards_won = ["None" for x in range(9)]
    while not os.path.exists("end_game"):
        if "NaturallyUnintelligent.go" and len(moves_taken) == 0 and os.path.exists("first_four_moves"):
            with open("first_four_moves", "r") as f:
                moves_taken = f.readlines()
                for val in moves_taken:
                    val_split = val.split()
                    if val_split[0] == "NaturallyUnintelligent":
                        update_board(player_symbol, coord_convert(val_split[1], val_split[2]))
                    else:
                        update_board(opponent_symbol, coord_convert(val_split[1], val_split[2]))
        if os.path.exists("NaturallyUnintelligent.go"):
            if canPlay:
                take_turn()
                canPlay = False
        else:
            canPlay = True
    exit()
