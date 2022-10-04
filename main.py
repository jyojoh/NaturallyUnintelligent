import sys
import os
import time

# Use symbols for setting board state
player_symbol = "O"
opponent_symbol = "X"
# Time limit to take a turn
time_limit = 10.0
# Used for first four moves to initialize board state
moves_taken = []
# Board state array
board_state = []
# Boards won array
boards_won = []

# Called when NaturallyUnintelligent.go exists
def take_turn():
    if os.path.exists("move_file"):
        # Set opponent move to what's in move_file
        with open("move_file") as f:
            opponent_move = f.readline()
        # Needs to set last move taken to the last move in first four moves if going first
        if os.path.getsize("move_file") == 0:
            opponent_move = moves_taken[3]
    # Parse move taken by opponent and update board state
    next_board = parse_move(opponent_move) % 9

    # get valid possible moves that can be made after updating board state
    next_moves = valid_moves(next_board)
    # Perform minimax on possible moves 
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
    i = int(i) # Sub-Board number, from 0-8
    j = int(j) # Sub-board coordinate, from 0-8
    return (i * 9) + j # Convert to number from 0 to 80


def parse_move(str):
    move = str.split()
    symbol = opponent_symbol

    if move[0] == "NaturallyUnintelligent":
        symbol = player_symbol

    sub_board = int(move[1])  # Sub-Board number, from 0-8
    board_coord = int(move[2])  # Sub-board coordinate, from 0-8

    # convert coordinate to board state index --> board state is an array from 0 to 80, convert from coord to integer index
    index = coord_convert(sub_board, board_coord)
    # Update board state with move parsed
    update_board(symbol, index)
    return index

# Update board state --> set given index of board state to given symbol (symbols defined in lines 6 and 7)
def update_board(symbol, index):
    board_state[index] = symbol
    # When updating board, check if a sub board was won
    check_win(index // 9, False)

# Checks if a given sub board was won, takes in a sub board and a boolean --> eval is true if we are just evaluating if a current move allows a win, false when we are planning on updating the board state 
# Boolean is to make sure we don't touch board state when evaluating in our heuristic
def check_win(sub_board, eval):
    # Don't check a sub board that was already won
    if boards_won[sub_board] != "None":
        return

    # Get center sub board index based on board state index (i.e. sub_board = 2: center_index in board_state = 22)
    center_index = sub_board * 9 + 4

    # If we are not evaluating and a sub board has been won, we want to fill the sub board in the board state so we don't try to play in the won board 
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

# Checks if given move blocks opponent from winning
# Performs check_win with opponent symbol --> if true, return true
def check_block(move):
    board_state[move] = opponent_symbol
    if check_win(move // 9, True):
        board_state[move] = "EMPTY"
        return True
    board_state[move] = "EMPTY"
    return False

# Fills sub board indexes in board state with string "Filled" to avoid trying to play in sub boards that have been won
def fill_subboard(sub_board):
    for idx in range(sub_board * 9, sub_board * 9 + 9):
        board_state[idx] = "Filled"
    print(str(sub_board) + " has been won.")

# Minimax takes in all possible moves, if it's the mins or maxs turn, the depth of the tree,...
# ...alpha, beta, the current best move, and the start time of take turn
def minimax(moveset, isMax, depth, a, b, best_move, start_time):
    bMove = best_move
    currSymbol = opponent_symbol

    # Part of heuristic to avoid expanding the tree the entire way if we think we're going to run out of time
    if time.time() - start_time >= time_limit - 0.1:
        print("No Time! Returning best move.")
        # Return current best move 
        return bMove
    # If we've gone down the tree the alotted depth, return the current best move
    if depth == 0:
        return bMove

    # Max's turn in minimax
    if isMax:
        currSymbol = player_symbol
        # Iterate through all possible moves in moveset given
        for move in moveset:
            # Perform heuristic on each move
            score = heuristic(move, currSymbol)
            # Part of alpha beta pruning
            # check if score given by heuristic is greater than current alpha, if so set alpha = score and set best move to current move
            if score > a:
                a = score
                bMove = move
            # Perform minimax again with new moves based on edited board state, Min's turn this time, subtract 1 from tree depth
            minimax(valid_moves(move % 9), not isMax, depth - 1, a, b, bMove, start_time)
            # Undo changes made to board state
            board_state[move] = "EMPTY"

            # alpha Beta pruning, makes sure to not expand tree nodes if the current alpha is greater than or equal to the current beta
            if a >= b:
                break

        return bMove

    # Min's turn in minimax
    else:
        currSymbol = opponent_symbol
        # Iterate through all possible moves in moveset given
        for idx, move in enumerate(moveset):
            # Perform heuristic on each move --> give negative score because it's opponent
            score = -heuristic(move, currSymbol)
            # If current score is less than Beta, set Beta equal to move score and best move to the current move
            if score < b:
                b = score
                bMove = move
            # Perform minimax again with new moves based on edited board state, Max's turn this time, subtract 1 from tree depth
            minimax(valid_moves(move % 9), not isMax, depth - 1, a, b, bMove, start_time)
            # Undo changes made to board state
            board_state[move] = "EMPTY"
            
            # alpha Beta pruning, makes sure to not expand tree nodes if the current alpha is greater than or equal to the current Beta
            if a >= b:
                break

        return bMove


def heuristic(move, symbol):
    move_score = 0
    board_state[move] = symbol

    # If this move wins us this local board, we want to take this move.
    if check_win(move // 9, True):
        move_score += 5

    # If the opponent would win by taking this move, we want to block them.
    if check_block(move):
        move_score += 3

    # If the opponent wins on the subsequent board in 1 move, don't send opponent to that board. This could allow them to win.
    if check_opponent_win(move):
        move_score -= 3
        if move % 9 == 4:
            move_score -= 1
        if check_win_big(move % 9):
            move_score -= 10

    # If player wins on subsequent board in 1 move, don't send opponent to that board. This could allow them to block us.
    if check_player_win(move):
        move_score -= 1
        if move // 9 == 4:
            move_score -= 1

    # Want to take center tile in sub-board.
    if move % 9 == 4:
        move_score += 1
        if move // 9 == 4:
            move_score += 1

    return move_score

# Check if move made will send opponent to a board the player can win
# Don't want opponent to block player win
def check_player_win(move):
    # Get next sub board
    sub_board = move % 9
    if boards_won[sub_board] != "None":
        return False
    check_moves = valid_moves(sub_board)
    
    # Check for win in valid moves of next sub board
    for index in range(len(check_moves)):
        board_state[check_moves[index]] = player_symbol
        if check_win(sub_board, True):
            board_state[check_moves[index]] = "EMPTY"
            return True
        board_state[check_moves[index]] = "EMPTY"
    return False

# Check if move made will send opponent to a board the opponent can win
# Don't want opponent to win next board
def check_opponent_win(move):
    # Get next sub board
    sub_board = move % 9
    if boards_won[sub_board] != "None":
        return False
    check_moves = valid_moves(sub_board)

    # Check for win in valid moves of next sub board
    for index in range(len(check_moves)):
        board_state[check_moves[index]] = opponent_symbol
        if check_win(sub_board, True):
            board_state[check_moves[index]] = "EMPTY"
            return True
        board_state[check_moves[index]] = "EMPTY"
    return False

# Check if opponent will win whole game given the next subboard of the move
def check_win_big(subboard):
    # Don't check if next subboard was already won
    if boards_won[subboard] != 'None':
        return False

    # Copy board won array to avoid editing the array
    boards_won_copy = boards_won.copy()
    boards_won_copy[subboard] = opponent_symbol

    if boards_won_copy[0] == opponent_symbol and boards_won_copy[3] == opponent_symbol and boards_won_copy[6] == opponent_symbol: # Left Column
        return True
    elif boards_won_copy[1] == opponent_symbol and boards_won_copy[4] == opponent_symbol and boards_won_copy[7] == opponent_symbol: # Middle Column
        return True
    elif boards_won_copy[2] == opponent_symbol and boards_won_copy[5] == opponent_symbol and boards_won_copy[8] == opponent_symbol: # Right Column
        return True
    elif boards_won_copy[0] == opponent_symbol and boards_won_copy[1] == opponent_symbol and boards_won_copy[2] == opponent_symbol: # Top Row
        return True
    elif boards_won_copy[3] == opponent_symbol and boards_won_copy[4] == opponent_symbol and boards_won_copy[5] == opponent_symbol: # Middle Row
        return True
    elif boards_won_copy[6] == opponent_symbol and boards_won_copy[7] == opponent_symbol and boards_won_copy[8] == opponent_symbol: # Bottom Row
        return True
    elif boards_won_copy[0] == opponent_symbol and boards_won_copy[4] == opponent_symbol and boards_won_copy[8] == opponent_symbol: # Left to Right diagonal
        return True
    elif boards_won_copy[2] == opponent_symbol and boards_won_copy[4] == opponent_symbol and boards_won_copy[6] == opponent_symbol: # Right to Left diagonal
        return True

    return False

# Identify valid moves a player can take using their next specified sub board
def valid_moves(next_board):
    moveset = []

    # Check if sub board was won already, if so, valid moves are any moves on boards that haven't been won yet 
    if boards_won[next_board] != "None":
        for index, tile in enumerate(board_state):
            if tile == "EMPTY":
                moveset.append(index)
        return moveset

    # get indexes of board state the sub board exists on 
    subboard_state = board_state[next_board * 9: next_board * 9 + 9]
    # Enumerate through sub board state to find moves that are empty
    for index, tile in enumerate(subboard_state):
        if tile == "EMPTY":
            moveset.append(index + (next_board * 9))

    if moveset == []:
        for index, tile in enumerate(board_state):
            if tile == "EMPTY":
                moveset.append(index)

    return moveset

# Main function
if __name__ == '__main__':
    canPlay = True
    # Init board state and boards won with dummy values
    board_state = ["EMPTY" for x in range(81)]
    boards_won = ["None" for x in range(9)]
    # Check that end_game does not exist in directory
    while not os.path.exists("end_game"):
        # Check that first_four_moves file exists
        if "NaturallyUnintelligent.go" and len(moves_taken) == 0 and os.path.exists("first_four_moves"):
            with open("first_four_moves", "r") as f:
                # Set moves_taken to array of lines from first_four_moves
                moves_taken = f.readlines()
                for val in moves_taken:
                    val_split = val.split()
                    # Update board state based on first_four_moves
                    if val_split[0] == "NaturallyUnintelligent":
                        update_board(player_symbol, coord_convert(val_split[1], val_split[2]))
                    else:
                        update_board(opponent_symbol, coord_convert(val_split[1], val_split[2]))
        # Check if "NaturallyUnintelligent.go" exists, if so then take turn
        if os.path.exists("NaturallyUnintelligent.go"):
            if canPlay:
                take_turn()
                canPlay = False
        else:
            canPlay = True
    exit()
