import random

class Player(object):
    def __init__(self, symbol):
        self._symbol = symbol

    def __str__(self):
        return self.symbol

    @property
    def symbol(self):
        return self._symbol

    def chooseMove(self, board):
        raise NotImplementedError

class Human(Player):
    def chooseMove(self, board):
        while True:
            move = raw_input('Enter your move: ')
            try:
                return board.getByHuman(move)
            except ValueError as e:
                print e

class Random(Player):
    def chooseMove(self, board):
        empties = list(board.emptySquares())
        square = random.choice(empties)
        return square

