import pygame as pg
import os
import math
import time
import numpy as np

from pieces import Square, Move

pieces = {0:'pawn', 1:'rook', 2:'knight', 3:'bishop', 4:'queen', 5:'king'}
letters = {0:'a', 1:'b', 2:'c',
                   3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}

def get_letter_coords(index):

    file = letters[index[0]]
    rank = str(8 - index[1])

    return(file+rank)

class Position:

    # Define the position at the start of the game using a FEN string
    STARTING_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    #STARTING_POSITION = '1n1qkbnr/1bpppppp/1p6/r3PK2/8/p7/PPPP1PPP/RNBQ1BNR'
    #STARTING_POSITION = '8/8/8/8/8/3k4/8/3K4'

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

    def toFen(self):

        result = ''
        empty_counter = 0
        letter = ''
        for j in range(0, 8):
            for i in range(0, 8):
                if not self.current[i][j].isOccupied():
                    empty_counter += 1
                else:
                    if self.current[i][j].get_piece() == 'pawn':
                        letter = 'p'
                    elif self.current[i][j].get_piece() == 'rook':
                        letter = 'r'
                    elif self.current[i][j].get_piece() == 'knight':
                        letter = 'n'
                    elif self.current[i][j].get_piece() == 'bishop':
                        letter = 'b'
                    elif self.current[i][j].get_piece() == 'queen':
                        letter = 'q'
                    elif self.current[i][j].get_piece() == 'king':
                        letter = 'k'
                    if not empty_counter == 0:
                        result = result + f'{empty_counter}'
                    if self.current[i][j].get_color() == 'white':
                        result = result + letter.capitalize()
                    else:
                        result = result + letter
                    empty_counter = 0
                if i == 7 and not empty_counter == 0:
                    result = result + f'{empty_counter}'
            if not j == 7:
                result = result + '/'
            empty_counter = 0

        return result


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
            elif origin.get_color() == 'black':
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
            return []


        ########################################
        ################# PAWN #################
        ########################################

        if target.get_piece() == 'pawn':
            if target.get_color() == 'white':

                if not self.current[index[0]][index[1] - 1].isOccupied():
                    legal_moves.append((index[0], index[1]-1))
                    if index[1] == 6 and not self.current[index[0]][index[1] - 2].isOccupied():
                        legal_moves.append((index[0], index[1] - 2))

                if (index[0]-1 >= 0) and (self.current[index[0]-1][index[1]-1].isOccupied())\
                    and (self.current[index[0]-1][index[1]-1].get_color() != target.get_color()):
                    legal_moves.append((index[0]-1, index[1]-1))
                if (index[0]+1 <= 7) and (self.current[index[0]+1][index[1]-1].isOccupied())\
                    and (self.current[index[0]+1][index[1]-1].get_color() != target.get_color()):
                    legal_moves.append((index[0]+1, index[1]-1))

                if len(moves) > 0 and moves[-1].get_piece() == 'pawn' and \
                        abs(moves[-1].get_target()[1] - moves[-1].get_origin()[1]) == 2 and \
                        index[1] == 3 and abs(moves[-1].get_target()[0] - index[0]) == 1:

                    direction = moves[-1].get_target()[0] - index[0]
                    self.move_piece(self.current[index[0]][3],
                                    self.current[index[0]+direction][2])
                    self.current[index[0]+direction][3] = \
                        Square(get_letter_coords((index[0]+direction, 3)))

                    if not self.newInCheck('white'):
                        legal_moves.append((moves[-1].get_target()[0], moves[-1].get_target()[1] - 1))

                    self.current[index[0] + direction][3] = \
                        Square(get_letter_coords((index[0]+direction, 3)), piece='pawn', color='black')
                    self.move_piece(self.current[index[0] + direction][2],
                                    self.current[index[0]][3])

            else:

                if index[1] + 1 < 8:
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

                    if len(moves) > 0 and moves[-1].get_piece() == 'pawn' and \
                            abs(moves[-1].get_target()[1] - moves[-1].get_origin()[1]) == 2 and \
                            index[1] == 4 and abs(moves[-1].get_target()[0] - index[0]) == 1:

                        direction = moves[-1].get_target()[0] - index[0]
                        self.move_piece(self.current[index[0]][4],
                                        self.current[index[0]+direction][5])
                        self.current[index[0]+direction][4] = \
                            Square(get_letter_coords((index[0]+direction, 4)))

                        if not self.newInCheck('black'):
                            legal_moves.append((moves[-1].get_target()[0], moves[-1].get_target()[1] + 1))

                        self.current[index[0] + direction][4] = \
                            Square(get_letter_coords((index[0]+direction, 4)), piece='pawn', color='white')
                        self.move_piece(self.current[index[0] + direction][5],
                                        self.current[index[0]][4])


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
        ########## CASTLING & CHECKS ###########
        ########################################

        # Remove all moves from the list that result in checks
        if look_for_checks:

            if white_turn:
                color = 'white'
            else:
                color = 'black'

            if target.get_piece() == 'king':
                if self.can_castle(white_turn, moves)[0] \
                        and not self.current[index[0] - 1][index[1]].isOccupied() \
                        and not self.current[index[0] - 2][index[1]].isOccupied() \
                        and not self.current[index[0] - 3][index[1]].isOccupied() \
                        and not self.newInCheck(color):

                    self.move_piece(self.current[index[0]][index[1]],
                                    self.current[index[0] - 1][index[1]])

                    if not self.newInCheck(color):
                        legal_moves.append((index[0] - 2, index[1]))

                    self.move_piece(self.current[index[0] - 1][index[1]],
                                    self.current[index[0]][index[1]])

                if self.can_castle(white_turn, moves)[1] \
                        and not self.current[index[0] + 1][index[1]].isOccupied() \
                        and not self.current[index[0] + 2][index[1]].isOccupied() \
                        and not self.newInCheck(color):

                    self.move_piece(self.current[index[0]][index[1]],
                                    self.current[index[0] + 1][index[1]])

                    if not self.newInCheck(color):
                        legal_moves.append((index[0] + 2, index[1]))

                    self.move_piece(self.current[index[0] + 1][index[1]],
                                    self.current[index[0]][index[1]])

            for move in list(legal_moves):

                target_square = Square(self.current[move[0]][move[1]].get_location(),
                                       self.current[move[0]][move[1]].get_piece(),
                                       self.current[move[0]][move[1]].get_color())

                self.move_piece(self.current[index[0]][index[1]], self.current[move[0]][move[1]])

                if self.newInCheck(color):
                    legal_moves.remove(move)

                self.move_piece(self.current[move[0]][move[1]], self.current[index[0]][index[1]])
                self.current[move[0]][move[1]] = target_square

        return(legal_moves)

    def newInCheck(self, color):

        king_index = self.get_king_pos(color)

        if color == 'white':
            white_turn = True
        elif color == 'black':
            white_turn = False
        else:
            return

        for i in range(0, 6):
            self.current[king_index[0]][king_index[1]].set_piece(pieces[i])
            attacks = self.get_moves(self.current[king_index[0]][king_index[1]], [],
                                        white_turn, look_for_checks=False)

            for attack in attacks:
                if self.current[attack[0]][attack[1]].get_piece() == pieces[i]:
                    self.current[king_index[0]][king_index[1]].set_piece('king')
                    return True

        self.current[king_index[0]][king_index[1]].set_piece('king')

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

    def drawByInsufficient(self):

        white_material = []
        black_material = []

        for i in range(0, 8):
            for j in range(0, 8):
                if self.current[i][j].get_piece() == 'pawn' or \
                        self.current[i][j].get_piece() == 'queen' or \
                        self.current[i][j].get_piece() == 'rook':
                    return False
                if not self.current[i][j].get_piece() == 'king':
                    if self.current[i][j].get_color() == 'white':
                        white_material.append(self.current[i][j].get_piece())
                    elif self.current[i][j].get_color() == 'black':
                        black_material.append(self.current[i][j].get_piece())

        if len(white_material) > 2 or len(black_material) > 2:
            return False

        if (len(white_material) == 2 and 'bishop' in white_material) or \
                (len(black_material) == 2 and 'bishop' in black_material):
            return False

        return True

    def drawByRepetition(self, fen_strings):

        count = 0

        for position in fen_strings:
            if position == self.toFen():
                count += 1
            if count > 2:
                return True

        return False

    def en_passant(self, moves):

        if moves[-1].get_piece() == 'pawn' and \
                moves[-1].get_origin()[0] != moves[-1].get_target()[0] and \
                not moves[-1].isCapture():
            return True

        return False