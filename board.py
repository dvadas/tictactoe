import itertools
import string

class Square(object):
    def __init__(self, i, indexes):
        self.player = None
        self.i = i
        self.indexes = indexes
        self._human = self._indexes2human(self.indexes)

    # Turn maths-friendly indexes into human-readable square names.
    # E.g. [0, 1] -> 'A2'
    def _indexes2human(self, indexes):
        labels = string.uppercase
        numLabels = string.digits[1:]
        human = []
        for index in indexes:
            human.append(labels[index])
            labels = numLabels
        return ''.join(human)

    def __str__(self):
        return '%s:%s' % (self._human, self.symbol)

    def empty(self):
        return self.player is None

    @property
    def human(self):
        return self._human

    @property
    def symbol(self):
        if self.empty():
            return ' '
        else:
            return self.player.symbol

class Board(object):
    def __init__(self, dimensions, size, winSize):
        self._dimensions = dimensions
        self._size = size
        self._winSize = winSize

        self._moves = []
        squareIndexes = itertools.product(xrange(size), repeat=dimensions)
        self._squares = [Square(i, indexes) for i, indexes in enumerate(squareIndexes)]

        directions = itertools.product([0, 1], repeat=dimensions)
        self._directions = []
        for direction in directions:
            if sum(direction) == 0:
                continue

            reverse = [-value for value in direction]
            self._directions.append((direction, reverse))

    def __str__(self):
        return ' '.join(str(square) for square in self._squares)

    def getByHuman(self, human):
        for square in self._squares:
            if square.human == human.upper():
                return square

        raise ValueError('invalid move: %s' % human)

    def apply(self, player, square):
        self._moves.append(square)
        square.player = player

    def finished(self):
        if len(self._moves) == len(self._squares):
            print 'draw'
            return True

        try:
            lastMove = self._moves[-1]
        except IndexError:
            return False

        player = lastMove.player
        for direction, reverse in self._directions:
            forwards = self._findLine(player, lastMove, direction)
            backwards = self._findLine(player, lastMove, reverse)
            if len(forwards) + len(backwards) + 1 >= self._winSize:
                winningLine = forwards + [lastMove] + backwards
                print 'winner:', player
                print ' '.join(map(str, winningLine))
                return True

        return False

    def _findLine(self, player, square, direction):
        sumIndexes = 0
        for index, digit in zip(square.indexes, direction):
            newIndex = index + digit
            if newIndex > self._size - 1 or newIndex < 0:
                return []

            sumIndexes *= self._size
            sumIndexes += newIndex

        newSquare = self._squares[sumIndexes]

        if newSquare.player is not player:
            return []

        result = self._findLine(player, newSquare, direction)
        result.append(newSquare)
        return result

    def emptySquares(self):
        for square in self._squares:
            if square.empty():
                yield square

