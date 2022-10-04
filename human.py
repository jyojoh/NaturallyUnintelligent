import pygame
import display as disp


# This function, naturally, depends on how the game is displayed to the user
# As long as the xy_to_global function works as intended, this will work fine
def human_player(moves, main_board, local_board_num, my_symbol, opponent_symbol):
    move_selected = False
    move = -1
    while not move_selected:
        xy = -1
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    xy = pygame.mouse.get_pos()
                    waiting = False

        move = disp.xy_to_global(xy)
        if move in moves:
            move_selected = True

    return move
