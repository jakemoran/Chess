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
            return(f'{self.get_color().capitalize()} {self.get_piece()} on {self.get_location()}')
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

        try:
            rank = 8 - int(rank)
        except(TypeError):
            print(self.location)
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

    def set_color(self, color):
        self.color = color
        return

    def isOccupied(self):
        return self.occupied


class Move:

    def __init__(self, piece, color, origin, target, is_capture=False, captured_piece=None,
                 en_passant=False, short_castle=False, long_castle=False):
        self.piece = piece
        self.color = color
        self.origin = origin
        self.target = target
        self.capture = is_capture
        self.captured_piece = captured_piece
        self.en_passant = en_passant
        self.short_castle = short_castle
        self.long_castle = long_castle


    def __repr__(self):

        if self.getEnPassant():
            return(f'{self.color.capitalize()} {self.piece} from {self.origin} to '
                   f'{self.target}. Captured a pawn en passant.')
        elif self.getShortCastle():
            return(f'{self.color.capitalize()} {self.piece} from {self.origin} to '
                   f'{self.target}. Short Castled.')
        elif self.getLongCastle():
            return(f'{self.color.capitalize()} {self.piece} from {self.origin} to '
                   f'{self.target}. Long Castled.')
        elif self.isCapture():
            return (f'{self.color.capitalize()} {self.piece} from {self.origin} to '
                    f'{self.target}. Captured a {self.getCapturedPiece()}')
        else:
            return (f'{self.color.capitalize()} {self.piece} from {self.origin} to {self.target}')


    def get_origin(self):
        return self.origin

    def get_target(self):
        return self.target

    def get_piece(self):
        return self.piece

    def get_color(self):
        return self.color

    def isCapture(self):
        return self.capture

    def getCapturedPiece(self):
        return self.captured_piece

    def getEnPassant(self):
        return self.en_passant

    def getShortCastle(self):
        return self.short_castle

    def getLongCastle(self):
        return self.long_castle

    def setMoveType(self, is_en_passant, is_short_castle, is_long_castle):
        self.en_passant = is_en_passant
        self.short_castle = is_short_castle
        self.long_castle = is_long_castle
