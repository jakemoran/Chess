import pygame as pg
import os
import math
import time
import numpy as np

BOARD_WIDTH, BOARD_HEIGHT = 640, 640

class Square:

    def __init__(self, location, piece='none', color='none', image=True):

        self.location = location
        self.piece = piece
        self.color = color

        if image and self.color != 'none' and self.piece != 'none':
            self.image = pg.image.load(os.path.join('Assets', f'{color+piece}.png'))
            self.occupied = True
        else:
            self.image = 'none'
            self.occupied = False

    def __repr__(self):
        if self.occupied:
            return(f'{self.get_color()} {self.get_piece()} on {self.get_location()}')
        else:
            return(f'{self.get_location()}: Empty')


    def get_coords(self):

        file = self.location[0:1]
        rank = self.location[1:2]

        if file == 'a':
            file = 0
        elif file == 'b':
            file = 1
        elif file == 'c':
            file = 2
        elif file == 'd':
            file = 3
        elif file == 'e':
            file = 4
        elif file == 'f':
            file = 5
        elif file == 'g':
            file = 6
        else:
            file = 7

        rank = 8 - int(rank)
        return (file*BOARD_WIDTH/8, rank*BOARD_HEIGHT/8)

    def get_index(self):

        file = math.floor(self.get_coords()[0] / (BOARD_WIDTH / 8))
        rank = math.floor(self.get_coords()[1] / (BOARD_HEIGHT / 8))

        return ((file, rank))

    def get_location(self):
        return self.location

    def get_piece(self):
        return self.piece

    def get_color(self):
        return self.color

    def get_image(self):
        return self.image

    def set_location(self, coords):
        self.location = coords
        return

    def set_image(self, image):
        self.image = image
        return

    def set_piece(self, piece):
        self.piece = piece
        return

    def isOccupied(self):
        return self.occupied


class Move:

    def __init__(self, piece, color, origin, target):
        self.piece = piece
        self.color = color
        self.origin = origin
        self.target = target


    def __repr__(self):
        return(f'{self.color} {self.piece} from {self.origin} to {self.target}')

    def get_origin(self):
        return self.origin

    def get_target(self):
        return self.target

    def get_piece(self):
        return self.piece

    def get_color(self):
        return self.color

class Position:

    # Define the position at the start of the game using a FEN string
    STARTING_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

    def __init__(self, position_id=STARTING_POSITION, lastmove=0, load_images=True):
        self.position_id = position_id
        self.lastmove = lastmove

        position_info = self.build_position(load_images)

        self.current = position_info[0]
        self.white_king_pos = position_info[1]
        self.black_king_pos = position_info[2]

    def build_position(self, load_images):

        file = 0
        rank = 0
        letters = {0:'a', 1:'b', 2:'c',
                   3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

        current_pos = [[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]]

        for i in range(0, len(current_pos)):
            for j in range(0, len(current_pos[0])):
                current_pos[i][j] = Square(letters[i]+str(8-j))

        for i in self.position_id:
            if i.isdigit():
                file += int(i) - 1
            elif i == '/':
                rank += 1
                file = 0
            elif i == 'r':
                current_pos[file][rank] = Square(letters[file]+str(8-rank),
                                                 piece='rook', color='black', image=load_images)
            elif i == 'n':
                current_pos[file][rank] = Square(letters[file]+str(8-rank),
                                                 piece='knight', color='black', image=load_images)
            elif i == 'b':
                current_pos[file][rank] = Square(letters[file]+str(8-rank),
                                                 piece='bishop', color='black', image=load_images)
            elif i == 'q':
                current_pos[file][rank] = Square(letters[file]+str(8-rank),
                                                 piece='queen', color='black', image=load_images)
            elif i == 'k':
                current_pos[file][rank] = Square(letters[file]+str(8-rank),
                                                 piece='king', color='black', image=load_images)
            elif i == 'p':
                current_pos[file][rank] = Square(letters[file]+str(8-rank),
                                                 piece='pawn', color='black', image=load_images)
            elif i == 'R':
                current_pos[file][rank] = Square(letters[file]+str(8-rank),
                                                 piece='rook', color='white', image=load_images)
            elif i == 'N':
                current_pos[file][rank] = Square(letters[file]+str(8-rank),
                                                 piece='knight', color='white', image=load_images)
            elif i == 'B':
                current_pos[file][rank] = Square(letters[file]+str(8-rank),
                                                 piece='bishop', color='white', image=load_images)
            elif i == 'Q':
                current_pos[file][rank] = Square(letters[file]+str(8-rank),
                                                 piece='queen', color='white', image=load_images)
            elif i == 'K':
                current_pos[file][rank] = Square(letters[file]+str(8-rank),
                                                 piece='king', color='white', image=load_images)
            elif i == 'P':
                current_pos[file][rank] = Square(letters[file]+str(8-rank),
                                                 piece='pawn', color='white', image=load_images)

            if i != '/':
                file += 1


        for i in range(0, 8):
            for j in range(0, 8):
                if current_pos[i][j].get_piece() == 'king':
                    if current_pos[i][j].get_color() == 'white':
                        white_king_pos = (i, j)
                    if current_pos[i][j].get_color() == 'black':
                        black_king_pos = (i, j)

        return current_pos, white_king_pos, black_king_pos

    def move_piece(self, origin, target):

        origin_ind = origin.get_index()
        target_ind = target.get_index()
        origin_location = origin.get_location()

        if not origin.isOccupied():
            print('No piece at origin')
            return

        if target.get_color() == origin.get_color():
            print('Origin and target location have the same color')
            return

        self.current[target_ind[0]][target_ind[1]] = self.current[origin_ind[0]][origin_ind[1]]
        self.current[target_ind[0]][target_ind[1]].set_location(target.get_location())
        self.current[origin_ind[0]][origin_ind[1]] = Square(origin_location)

        if origin.get_piece() == 'king':
            if origin.get_color() == 'white':
                self.white_king_pos = target_ind
            if origin.get_color() == 'black':
                self.black_king_pos = target_ind

        return

    def get_current_pos(self):
        return self.current

    def update_position(self, position):
        self.current = position
        return

    def get_last_move(self):
        return self.lastmove

    def set_last_move(self, move):
        self.lastmove = move
        return

    def get_king_pos(self, color):
        if color == 'white':
            return self.white_king_pos
        elif color == 'black':
            return self.black_king_pos

    def set_king_pos(self, color, index):

        if color == 'white':
            self.white_king_pos = index
        elif color == 'black':
            self.black_king_pos = index
        return

    def can_castle(self, white_turn, moves):

        can_castle_long = True
        can_castle_short = True

        if white_turn:
            color = 'white'
        else:
            color = 'black'

        for move in moves:
            if move.get_piece() == 'rook' and move.get_origin()[0] == 0 \
                    and move.get_color() == color:
                can_castle_long = False
            elif move.get_piece() == 'rook'and move.get_origin()[0] == 7 \
                    and move.get_color() == color:
                can_castle_short = False
            elif move.get_piece() == 'king' and move.get_color() == color:
                can_castle_long = False
                can_castle_short = False

        if color == 'white':
            if self.current[0][7].get_piece() != 'rook':
                can_castle_long = False
            if self.current[7][7].get_piece() != 'rook':
                can_castle_short = False
        else:
            if self.current[0][0].get_piece() != 'rook':
                can_castle_long = False
            if self.current[7][0].get_piece() != 'rook':
                can_castle_short = False


        return(can_castle_long, can_castle_short)

    # Generate a list of all the possible moves for a given piece, ignoring check.
    def get_moves(self, target, moves, white_turn, look_for_checks=True):

        index = target.get_index()
        legal_moves = []

        if target.get_color() == 'none' or target.get_piece() == 'none':
            print('What? How did this even happen?')
            return


        ########################################
        ################# PAWN #################
        ########################################

        if target.get_piece() == 'pawn':
            if target.get_color() == 'white':

                if not self.current[index[0]][index[1]-1].isOccupied():
                    legal_moves.append((index[0], index[1]-1))
                    if index[1] == 6 and not self.current[index[0]][index[1] - 2].isOccupied():
                        legal_moves.append((index[0], index[1] - 2))

                if (index[0]-1 >= 0) and (self.current[index[0]-1][index[1]-1].isOccupied())\
                    and (self.current[index[0]-1][index[1]-1].get_color() != target.get_color()):
                    legal_moves.append((index[0]-1, index[1]-1))
                if (index[0]+1 <= 7) and (self.current[index[0]+1][index[1]-1].isOccupied())\
                    and (self.current[index[0]+1][index[1]-1].get_color() != target.get_color()):
                    legal_moves.append((index[0]+1, index[1]-1))

            elif target.get_color() == 'black':

                if not self.current[index[0]][index[1] + 1].isOccupied():
                    legal_moves.append((index[0], index[1] + 1))
                    if index[1] == 1 and not self.current[index[0]][index[1] + 2].isOccupied():
                        legal_moves.append((index[0], index[1] + 2))

                if (index[0]-1 >= 0) and (self.current[index[0]-1][index[1]+1].isOccupied())\
                    and (self.current[index[0]-1][index[1]+1].get_color() != target.get_color()):
                    legal_moves.append((index[0]-1, index[1]+1))
                if (index[0]+1 <= 7) and (self.current[index[0]+1][index[1]+1].isOccupied())\
                    and (self.current[index[0]+1][index[1]+1].get_color() != target.get_color()):
                    legal_moves.append((index[0]+1, index[1]+1))


        ########################################
        ######## QUEEN, KING, and ROOK #########
        ########################################

        if target.get_piece() == 'queen' or \
            target.get_piece() == 'king' or \
            target.get_piece() == 'rook':

            kingMove = True

            # Up moves
            for i in range(1, 8):

                if index[1] - i < 0:
                    break
                if target.get_piece() == 'king' and not kingMove:
                    break
                if self.current[index[0]][index[1] - i].isOccupied():
                    if self.current[index[0]][index[1] - i].get_color() != target.get_color():
                        legal_moves.append((index[0], index[1] - i))
                        break
                    else:
                        break
                legal_moves.append((index[0], index[1] - i))
                kingMove = False

            kingMove = True

            # Down moves
            for i in range(1, 8):

                if index[1] + i > 7:
                    break
                if target.get_piece() == 'king' and not kingMove:
                    break
                if self.current[index[0]][index[1] + i].isOccupied():
                    if self.current[index[0]][index[1] + i].get_color() != target.get_color():
                        legal_moves.append((index[0], index[1] + i))
                        break
                    else:
                        break
                legal_moves.append((index[0], index[1] + i))
                kingMove = False

            kingMove = True

            # Left moves
            for i in range(1, 8):

                if index[0] - i < 0:
                    break
                if target.get_piece() == 'king' and not kingMove:
                    break
                if self.current[index[0] - i][index[1]].isOccupied():
                    if self.current[index[0] - i][index[1]].get_color() != target.get_color():
                        legal_moves.append((index[0] - i, index[1]))
                        break
                    else:
                        break
                legal_moves.append((index[0] - i, index[1]))
                kingMove = False

            kingMove = True

            # Right moves
            for i in range(1, 8):

                if index[0] + i > 7:
                    break
                if target.get_piece() == 'king' and not kingMove:
                    break
                if self.current[index[0] + i][index[1]].isOccupied():
                    if self.current[index[0] + i][index[1]].get_color() != target.get_color():
                        legal_moves.append((index[0] + i, index[1]))
                        break
                    else:
                        break
                legal_moves.append((index[0] + i, index[1]))
                kingMove = False

        ########################################
        ####### QUEEN, KING, and BISHOP ########
        ########################################

        if target.get_piece() == 'queen' or \
                target.get_piece() == 'king' or \
                target.get_piece() == 'bishop':

            kingMove = True

            # Up-Left moves
            for i in range(1, 8):

                if index[1] - i < 0 or index[0] - i < 0:
                    break
                if target.get_piece() == 'king' and not kingMove:
                    break
                if self.current[index[0] - i][index[1] - i].isOccupied():
                    if self.current[index[0] - i][index[1] - i].get_color() != target.get_color():
                        legal_moves.append((index[0] - i, index[1] - i))
                        break
                    else:
                        break
                legal_moves.append((index[0] - i, index[1] - i))
                kingMove = False

            kingMove = True

            # Down-Left moves
            for i in range(1, 8):

                if index[1] + i > 7 or index[0] - i < 0:
                    break
                if target.get_piece() == 'king' and not kingMove:
                    break
                if self.current[index[0] - i][index[1] + i].isOccupied():
                    if self.current[index[0] - i][index[1] + i].get_color() != target.get_color():
                        legal_moves.append((index[0] - i, index[1] + i))
                        break
                    else:
                        break
                legal_moves.append((index[0] - i, index[1] + i))
                kingMove = False

            kingMove = True

            # Up-Right moves
            for i in range(1, 8):

                if index[1] - i < 0 or index[0] + i > 7:
                    break
                if target.get_piece() == 'king' and not kingMove:
                    break
                if self.current[index[0] + i][index[1] - i].isOccupied():
                    if self.current[index[0] + i][index[1] - i].get_color() != target.get_color():
                        legal_moves.append((index[0] + i, index[1] - i))
                        break
                    else:
                        break
                legal_moves.append((index[0] + i, index[1] - i))
                kingMove = False

            kingMove = True

            # Down-Right moves
            for i in range(1, 8):

                if index[1] + i > 7 or index[0] + i > 7:
                    break
                if target.get_piece() == 'king' and not kingMove:
                    break
                if self.current[index[0] + i][index[1] + i].isOccupied():
                    if self.current[index[0] + i][index[1] + i].get_color() != target.get_color():
                        legal_moves.append((index[0] + i, index[1] + i))
                        break
                    else:
                        break
                legal_moves.append((index[0] + i, index[1] + i))
                kingMove = False

        ########################################
        ################ KNIGHT ################
        ########################################

        if target.get_piece() == 'knight':

            for i in range(-2, 3):
                for j in range(-2, 3):
                    if 0 <= index[0]+i <= 7 and 0 <= index[1] + j <= 7:
                        if abs(i) != abs(j) and i != 0 and j != 0:
                            if self.current[index[0] + i][index[1] + j].isOccupied()\
                                and self.current[index[0] + i][index[1] + j].get_color() != target.get_color():
                                legal_moves.append((index[0] + i, index[1] + j))
                            elif not self.current[index[0] + i][index[1] + j].isOccupied():
                                legal_moves.append((index[0] + i, index[1] + j))


        ########################################
        ############### CASTLING ###############
        ########################################

        if target.get_piece() == 'king':
            if self.can_castle(white_turn, moves)[0]\
                and not self.current[index[0] - 1][index[1]].isOccupied()\
                and not self.current[index[0] - 2][index[1]].isOccupied()\
                and not self.current[index[0] - 3][index[1]].isOccupied():

                legal_moves.append((index[0] - 2, index[1]))

            if self.can_castle(white_turn, moves)[1]\
                and not self.current[index[0] + 1][index[1]].isOccupied()\
                and not self.current[index[0] + 2][index[1]].isOccupied():

                legal_moves.append((index[0] + 2, index[1]))

        # Remove all moves from the list that result in checks
        if look_for_checks:
            for move in list(legal_moves):

                target_square = Square(self.current[move[0]][move[1]].get_location(),
                                       self.current[move[0]][move[1]].get_piece(),
                                       self.current[move[0]][move[1]].get_color())

                self.move_piece(self.current[index[0]][index[1]], self.current[move[0]][move[1]])

                if white_turn:
                    if self.inCheck('white', moves):
                        legal_moves.remove(move)
                else:
                    if self.inCheck('black', moves):
                        legal_moves.remove(move)

                self.move_piece(self.current[move[0]][move[1]], self.current[index[0]][index[1]])
                self.current[move[0]][move[1]] = target_square

        return(legal_moves)


    def inCheck(self, color, moves):

        king_index = self.get_king_pos(color)

        if color == 'white':
            white_turn = False
        elif color == 'black':
            white_turn = True
        else:
            return

        for i in range(0, 8):
            for j in range(0, 8):
                if self.current[i][j].isOccupied() and self.current[i][j].get_color() != color:
                    attacks = self.get_moves(self.current[i][j], moves,
                                             white_turn, look_for_checks=False)
                    for attack in attacks:
                        if attack == king_index:
                            return True

        return False

    def get_all_legal_moves(self, check_color, moves, white_turn):

        all_legal_moves = []
        for i in range(0, 8):
            for j in range(0, 8):
                if self.current[i][j].get_color() == check_color:
                    piece_moves = self.get_moves(self.current[i][j], moves, white_turn)
                    if piece_moves != []:
                        all_legal_moves.extend(piece_moves)

        return all_legal_moves
