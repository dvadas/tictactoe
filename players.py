import random

class Player(object):
    def __init__(self, symbol, number):
        self._symbol = symbol
        self._number = number
        self._string = 'Player %d (%s)' % (number, symbol)

    def __str__(self):
        return self._string

    @property
    def symbol(self):
        return self._symbol

    @property
    def number(self):
        return self._number

    def chooseMove(self, board):
        raise NotImplementedError

class Human(Player):
    def chooseMove(self, board):
        while True:
            move = raw_input('Enter your move: ')
            try:
                square = board.getByHuman(move)
            except ValueError as e:
                print e

            if square.empty():
                break
            print 'invalid move: %s is already taken' % move

        return square


class Random(Player):
    def chooseMove(self, board):
        empties = list(board.emptySquares())
        square = random.choice(empties)
        return square

