import numpy as np
import pygame
import core_gameplay as gp

#  VARIABLES
SCREEN_SIDE = 500
SCREEN_WIDTH = SCREEN_SIDE
SCREEN_HEIGHT = SCREEN_SIDE
SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
OVERLAYER = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
SQUARE_SIDE = int(SCREEN_SIDE/9)
P0_COLOR = (0, 0, 255)
P1_COLOR = (255, 165, 0)
X_OFFSET = 0
Y_OFFSET = 0


# Returns the x, y positions in screen space of the top left corner of the
# square representing the global space given
def global_to_xy(move):
    square_num, board_num = gp.global_to_local(move)

    # TODO Make these local xy converters separate functions
    yls = int(np.floor(square_num / 3))
    xls = square_num - yls * 3

    ylb = int(np.floor(board_num / 3))
    xlb = board_num - ylb * 3

    x = X_OFFSET + 3 * SQUARE_SIDE * xlb + SQUARE_SIDE * xls
    y = Y_OFFSET + 3 * SQUARE_SIDE * ylb + SQUARE_SIDE * yls
    return [x, y]


# Converts the x, y coordinate of screen space to a 0-80 global position on the board
def xy_to_global(xy):
    x, y = xy
    x = x - X_OFFSET
    y = y - Y_OFFSET

    ylb = np.floor(y / (3 * SQUARE_SIDE))
    xlb = np.floor(x / (3 * SQUARE_SIDE))

    yls = np.floor((y - ylb * 3 * SQUARE_SIDE) / SQUARE_SIDE)
    xls = np.floor((x - xlb * 3 * SQUARE_SIDE) / SQUARE_SIDE)

    return gp.local_to_global([xy_to_global_3x3(xls, yls), xy_to_global_3x3(xlb, ylb)])


# Converts the x, y positions of a 3x3 board to a 0-8 position
def xy_to_global_3x3(x, y):
    return 3 * y + x


def wait_for_player_press():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                waiting = False


# (left, top, width, height)
def draw_3x3_board(board, x, y):
    for i in range(0, 3):
        for j in range(0, 3):
            pygame.draw.rect(SCREEN, (255, 255, 255),
                             (x + i * SQUARE_SIDE, y + j * SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE))
            pygame.draw.rect(SCREEN, (0, 0, 0),
                             (x + i * SQUARE_SIDE, y + j * SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE), width=1)

            if board[3 * j + i] == gp.PLAYER0_MARKER:
                pygame.draw.circle(SCREEN, P0_COLOR,
                                   (x + i * SQUARE_SIDE + SQUARE_SIDE / 2, y + j * SQUARE_SIDE + SQUARE_SIDE / 2),
                                   SQUARE_SIDE / 2 * 0.9)

            if board[3 * j + i] == gp.PLAYER1_MARKER:
                pygame.draw.circle(SCREEN, P1_COLOR,
                                   (x + i * SQUARE_SIDE + SQUARE_SIDE / 2, y + j * SQUARE_SIDE + SQUARE_SIDE / 2),
                                   SQUARE_SIDE / 2 * 0.9)


def draw_big_board(bb, x, y):
    for i in range(0, 3):
        for j in range(0, 3):
            draw_3x3_board(bb[3 * j + i], x + 3 * i * SQUARE_SIDE, y + 3 * j * SQUARE_SIDE)


# Draws an overlay over board number local_num
# on big board with top left at x, y
def draw_board_overlay(local_num, x, y, color):
    yl = int(np.floor(local_num / 3))
    xl = local_num - yl * 3
    pygame.draw.rect(OVERLAYER, color,
                     (x + 3 * xl * SQUARE_SIDE, y + 3 * yl * SQUARE_SIDE, 3 * SQUARE_SIDE, 3 * SQUARE_SIDE))


#  Colors an overlay over all sub-boards that have been won
#  Colors based on the winner of the board
def overlay_decided(board_wins, x, y):
    for i in range(0, 9):
        marker = board_wins[i]
        if marker == gp.PLAYER0_MARKER:
            # TODO make based on color variables
            color = (0, 0, 255, 100)
        elif marker == gp.PLAYER1_MARKER:
            color = (255, 165, 0, 100)
        elif marker == gp.DRAW:
            color = (0, 0, 0, 100)
        else:
            continue

        draw_board_overlay(i, x, y, color)


def draw_game_board(main_board, main_board_wins, current_local_board, X_OFFSET, Y_OFFSET):
    draw_big_board(main_board, X_OFFSET, Y_OFFSET)
    OVERLAYER.fill((0, 0, 0, 0))
    overlay_decided(main_board_wins, X_OFFSET, Y_OFFSET)
    draw_board_overlay(current_local_board, X_OFFSET, Y_OFFSET, (255, 255, 0, 100))
    SCREEN.blit(OVERLAYER, (0, 0))
    pygame.display.flip()