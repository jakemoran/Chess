import pygame as pg
import math
import timeit
import time
import os

from pieces import Square, Move
from board import Position
from pygame import mixer
from pygame import gfxdraw


WIDTH, HEIGHT = 640, 640
BOARD_WIDTH, BOARD_HEIGHT = 640, 640
LIGHT_COLOR = (230, 210, 170)
DARK_COLOR = (133, 94, 66)
HIGHLIGHT = (0, 0, 0, 128)
LASTMOVE_COLOR = (255, 255, 0, 64)
BACKGROUND_COLOR = (0, 0, 0)

FPS = 120

letters = {0:'a', 1:'b', 2:'c',
                   3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

WIN = pg.display.set_mode((WIDTH, HEIGHT))
mixer.init()
pg.display.set_caption('')


# Scale a piece image to fit the size of the square
def scale(image):
    return pg.transform.smoothscale(image, (int(BOARD_WIDTH/8), int(BOARD_HEIGHT/8)))

# Draw the empty board
def draw_board(position_array, moves):

    # Set background color
    WIN.fill(BACKGROUND_COLOR)

    # Draw light and dark squares
    for i in range(0, 8):
        for j in range(0, 8):
            corner = [i * BOARD_WIDTH/8, j * BOARD_HEIGHT/8]
            square = pg.Rect(corner[0], corner[1], BOARD_WIDTH/8, BOARD_HEIGHT/8)

            # Square is light when rank and file have same parity
            if (i + 1) % 2 == (j + 1) % 2:
                pg.draw.rect(WIN, LIGHT_COLOR, square)
            else:
                pg.draw.rect(WIN, DARK_COLOR, square)


# Get coordinates of the nearest square to a set of pixel coordinates
# in file-rank notation
def get_nearest_square(coords):

    file = math.floor(coords[0]/(BOARD_WIDTH/8))
    file = letters[file]
    rank = str(8 - math.floor(coords[1]/(BOARD_HEIGHT/8)))

    return(file+rank)

# Get index of the nearest square to a set of pixel coordinates. (0,0) is top left
# and the array has the form (column, row)
def get_index(coords):

    file = math.floor(coords[0] / (BOARD_WIDTH / 8))
    rank = math.floor(coords[1] / (BOARD_HEIGHT / 8))

    return ((file, rank))

# Get coordinates of a square index in file-rank notation
def get_letter_coords(index):

    file = letters[index[0]]
    rank = str(8 - index[1])

    return(file+rank)

def positionGenerator(position, depth, color, white_turn):
    if depth == 1:
        return 1

    moves = position.get_all_legal_moves(color, [], white_turn)
    if color == 'white':
        for move in moves:
            position.move_piece()

def main():

    run = True
    clock = pg.time.Clock()
    dragging = False
    white_turn = True
    timing = False
    debug = True
    game_over = False

    # Initialize starting position, position array, and list of moves
    game_position = Position()
    position_array = game_position.get_current_pos()
    moves = []
    fen_strings = [game_position.toFen()]
    moves_since_last_capture = 0

    if debug:
        print(position_array)

    while run:
        clock.tick(FPS)

        for event in pg.event.get():

            if event.type == pg.QUIT:
                run = False

            elif event.type == pg.MOUSEBUTTONDOWN:
                if not game_over:

                    # Get information about what was clicked on
                    click = pg.mouse.get_pos()
                    click_ind = get_index(click)
                    click_coords = get_nearest_square(click)
                    click_square = position_array[click_ind[0]][click_ind[1]]

                    if debug:
                        print(click, get_index(click), get_nearest_square(click))
                        print(position_array[get_index(click)[0]][get_index(click)[1]])

                    # If it is a piece that can be moved, start dragging and calculate
                    # the legal moves
                    if (click_square.get_color() == 'white' and white_turn) \
                        or (click_square.get_color() == 'black' and not white_turn):

                        dragging = True

                        # Calculate the legal moves for the piece that was picked up
                        legal_moves = game_position.get_moves(click_square, moves, white_turn)

                        # Clear the origin square of the piece
                        position_array[click_ind[0]][click_ind[1]] = Square(click_coords)

            elif event.type == pg.MOUSEBUTTONUP:
                if dragging:

                    # Get parameters of target square
                    target_ind = get_index(pg.mouse.get_pos())
                    target_coords = get_nearest_square(pg.mouse.get_pos())

                    # Determine if the target square is a legal move
                    if target_ind in legal_moves:

                        capture = position_array[target_ind[0]][target_ind[1]].isOccupied()
                        captured_piece = position_array[target_ind[0]][target_ind[1]].get_piece()
                        en_passant = False
                        short_castle = False
                        long_castle = False

                        # If so update the target location with the piece that moved to it
                        position_array[target_ind[0]][target_ind[1]] = \
                            Square(target_coords, click_square.get_piece(), click_square.get_color())

                        # Store the move in the move list
                        this_move = Move(click_square.get_piece(), click_square.get_color(),
                                         click_ind, target_ind, capture, captured_piece)
                        moves.append(this_move)

                        # Castle the king if necessary
                        if this_move.get_piece() == 'king':

                            if this_move.get_origin()[0] - this_move.get_target()[0] == 2:

                                game_position.move_piece(position_array[0][target_ind[1]],
                                                         position_array[3][target_ind[1]])
                                long_castle = True

                            elif this_move.get_origin()[0] - this_move.get_target()[0] == -2:

                                game_position.move_piece(position_array[7][target_ind[1]],
                                                         position_array[5][target_ind[1]])
                                short_castle = True

                            if this_move.get_color() == 'white':
                                game_position.set_king_pos('white', target_ind)
                            elif this_move.get_color() == 'black':
                                game_position.set_king_pos('black', target_ind)

                        if this_move.get_piece() == 'pawn' and \
                            (this_move.get_target()[1] == 0 or this_move.get_target()[1] == 7):

                            position_array[target_ind[0]][target_ind[1]].set_piece('queen')
                            position_array[target_ind[0]][target_ind[1]].set_image(
                                pg.image.load(os.path.join('Assets', f'{this_move.get_color()}queen.png')))

                        if game_position.en_passant(moves):
                            capture = True
                            en_passant = True
                            position_array[moves[-2].get_target()[0]][moves[-2].get_target()[1]] = \
                                Square(get_letter_coords(moves[-2].get_target()))

                        this_move.setMoveType(en_passant, short_castle, long_castle)

                        if capture:
                            capture_sound = mixer.Sound(os.path.join('Assets', 'capture_piece.ogg'))
                            capture_sound.play()
                            moves_since_last_capture = 0
                        else:
                            move_sound = mixer.Sound(os.path.join('Assets', 'move_piece.ogg'))
                            move_sound.play()
                            moves_since_last_capture += 1

                        if white_turn:
                            white_turn = False
                            check_color = 'black'
                        else:
                            white_turn = True
                            check_color = 'white'

                        # Look for checks/checkmate/stalemate
                        number_of_moves = len(game_position.get_all_legal_moves(check_color,
                                                                                moves, white_turn))
                        fen_strings.append(game_position.toFen())

                        if debug:
                            print(this_move)
                            print(fen_strings[-1])

                        if game_position.newInCheck(check_color):
                            if number_of_moves == 0:
                                print('Checkmate!')
                                game_over = True
                            else:
                                print(f'{check_color.capitalize()} is in check')
                        else:
                            if number_of_moves == 0:
                                print('Draw by stalemate!')
                                game_over = True

                        if game_position.drawByInsufficient():
                            print('Draw by insufficient material!')
                            game_over = True

                        if game_position.drawByRepetition(fen_strings):
                            print('Draw by Repetition!')
                            game_over = True

                        if moves_since_last_capture == 100:
                            print('Draw by 50 move rule!')
                            game_over = True


                    else:
                        position_array[click_ind[0]][click_ind[1]] = click_square
                    dragging = False

                if timing:
                    start = time.time()
                    for i in range(0, 1):
                        if white_turn:
                            test = game_position.get_all_legal_moves('white',
                                                                     moves, white_turn)
                        else:
                            test = game_position.get_all_legal_moves('black',
                                                                     moves, white_turn)
                    print(time.time() - start)


        # Update the position and draw the blank board
        game_position.update_position(position_array)
        draw_board(position_array, moves)

        # Highlight last move
        if len(moves) > 0:
            last_move = moves[-1]
            origin_corner = [last_move.get_origin()[0] * BOARD_WIDTH / 8,
                             last_move.get_origin()[1] * BOARD_HEIGHT / 8]
            target_corner = [last_move.get_target()[0] * BOARD_WIDTH / 8,
                             last_move.get_target()[1] * BOARD_HEIGHT / 8]
            move_marker = pg.Surface((BOARD_WIDTH / 8, BOARD_HEIGHT / 8), pg.SRCALPHA)
            move_marker.fill(LASTMOVE_COLOR)
            WIN.blit(move_marker, origin_corner)
            WIN.blit(move_marker, target_corner)

        # Draw pieces
        for rank in position_array:
            for square in rank:
                if square.isOccupied():
                    WIN.blit(scale(square.get_image()), square.get_coords())

        # Draw piece on cursor if it is in the process of being moved and show
        # legal moves
        if dragging:
            if click_square.get_image() != 'none':
                for i in legal_moves:
                    corner = [int(i[0] * BOARD_WIDTH/8),
                              int(i[1] * BOARD_HEIGHT/8)]
                    center = [int(BOARD_WIDTH/16), int(BOARD_HEIGHT/16)]
                    marker = pg.Surface((BOARD_WIDTH/8, BOARD_HEIGHT/8), pg.SRCALPHA)
                    gfxdraw.aacircle(marker, center[0], center[1], int(BOARD_WIDTH/32), HIGHLIGHT)
                    gfxdraw.filled_circle(marker, center[0], center[1], int(BOARD_WIDTH/32), HIGHLIGHT)
                    WIN.blit(marker, corner)

                WIN.blit(scale(click_square.get_image()),
                         (pg.mouse.get_pos()[0]-BOARD_WIDTH/16,
                          pg.mouse.get_pos()[1]-BOARD_HEIGHT/16))

        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()
