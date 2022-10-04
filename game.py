import numpy as np
import pygame
import core_gameplay as gp
import display as disp

# Each AI function will have its own file to allow for more modular creation
import human


def nums_output(nums, p1_name, p2_name):
    symbols = [p1_name, p2_name]
    s = ''
    i = 0
    j = 1
    p = 0
    while i < 4:
        board = nums[i]
        spot = nums[j]
        s += symbols[p] + " " + str(board) + " " + str(spot) + '\n'
        p += 1
        p %= 2
        i += 1
        j += 1
    return s


class Game:
    def __init__(self, f_p1, f_p2, p1_name=None, p2_name=None, rand_start=False):
        self.names = [gp.PLAYER0_MARKER if p1_name is None else p1_name,
                      gp.PLAYER1_MARKER if p2_name is None else p2_name]
        self.f_p1 = f_p1
        self.f_p2 = f_p2
        # Initialize empty game state
        self.main_board = np.zeros((9, 9))
        self.main_board_wins = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.current_local_board = gp.NO_LOCAL_BOARD

        # Allows to easily change players and markers
        self.current_player = 0
        self.markers = [gp.PLAYER0_MARKER, gp.PLAYER1_MARKER]
        self.winner = gp.NO_MARKER

        # Optional Rule Variables

        # True allows you to send opponents to won boards (Thad rules)
        # False means won boards are off limits (Classic rules)
        self.can_move_in_won_board = False

        # True makes the game a draw when a player is sent to a full square (Thad rules)
        # False allows the player to play in any free space (Classic rules)
        self.send_to_full_board_is_draw = False

        #  Pygame initialization
        pygame.init()

        if rand_start:
            nums = gp.get_init_random_string()
            ffm = open("first_four_moves", "w")
            ffm.write(nums_output(nums, p1_name, p2_name))
            ffm.close()
            i = 0
            j = 1
            p = 0
            while i < 4:
                board = nums[i]
                spot = nums[j]
                gp.handle_mark_big_board(self.main_board, gp.local_to_global((spot, board)), self.markers[p],
                                         self.main_board_wins)
                p += 1
                p %= 2
                i += 1
                j += 1
            self.current_local_board = nums[i]

    def run(self):
        #  Drawing function
        disp.draw_game_board(self.main_board, self.main_board_wins, self.current_local_board, disp.X_OFFSET,
                             disp.Y_OFFSET)
        # GAME LOOP
        running = True
        while running:

            if self.winner != gp.NO_MARKER:
                self.end_game()
                continue

            current_marker = self.markers[self.current_player]
            all_moves = gp.valid_moves(self.main_board, self.current_local_board, self.can_move_in_won_board)

            if self.current_player == 0:
                selected_move = self.f_p1(all_moves, self.main_board, self.current_local_board,
                                          gp.PLAYER0_MARKER, gp.PLAYER1_MARKER)
            else:
                selected_move = self.f_p2(all_moves, self.main_board, self.current_local_board,
                                          gp.PLAYER1_MARKER, gp.PLAYER0_MARKER)

            try:
                move = int(selected_move)
            except TypeError:
                # there was a bad move given
                sig, msg = selected_move
                if sig == gp.BAD_MOVE_I_WIN:
                    self.winner = gp.MARKERS[self.current_player]
                elif sig == gp.BAD_MOVE_I_LOST:
                    self.winner = gp.MARKERS[(self.current_player + 1) % 2]
                elif sig == gp.BAD_MOVE_DRAW:
                    self.winner = gp.DRAW
                self.end_game(reason=msg)
                running = False
                continue
            else:
                selected_move = move

            # move local pair
            move_lp = gp.global_to_local(selected_move)
            local_sq = move_lp[0]

            if gp.handle_mark_big_board(self.main_board, selected_move, current_marker, self.main_board_wins) > -1:
                self.winner = gp.check_3x3_win(self.main_board_wins)

            print(self.main_board)

            # Change global-local board to local move value from last time IF it has valid moves
            if len(gp.valid_moves_3x3(self.main_board[local_sq], self.can_move_in_won_board)) > 0:
                self.current_local_board = local_sq
            elif self.send_to_full_board_is_draw:
                self.winner = gp.DRAW
                # For display purposes
                self.current_local_board = gp.NO_LOCAL_BOARD
            else:
                self.current_local_board = gp.NO_LOCAL_BOARD

            self.current_player = int((self.current_player + 1) % 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    continue

            #  Drawing function
            disp.draw_game_board(self.main_board, self.main_board_wins, self.current_local_board, disp.X_OFFSET,
                                 disp.Y_OFFSET)

    def current_player_name(self) -> str:
        return str(self.names[int(self.current_player - 1)])

    def end_game(self, reason=None):

        if self.winner > gp.DRAW:
            print("Player " + str(self.names[int(self.winner - 1)]) + " wins")
            w = str(self.names[int(self.winner - 1)])
            L = str(self.names[(int(self.winner - 1) + 1) % 2])
            if reason is None:
                reason = "The winning player has won 3 local boards in a row on the global board!"
            msg = f"END: {w} WINS! {L} LOSES! " + reason
        else:
            msg = "END: Match TIED!"
        eg = open("end_game", "w")
        eg.write(msg)
        print(msg)
        eg.close()
        open("{p}.go".format(p=self.names[0]), "w").close()
        open("{p}.go".format(p=self.names[1]), "w").close()
        disp.wait_for_player_press()


if __name__ == "__main__":
    game = Game(human.human_player, human.human_player, p1_name='Player 1', p2_name='Player 2', rand_start=True)
    game.run()
