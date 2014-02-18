#!/usr/bin/env python

import itertools
import optparse

from players import Player, Human, Random
from board import Board, Square

def main():
    optparser = optparse.OptionParser('usage: %prog [options]')
    optparser.add_option('-d', '--dimensions', type=int, default=2)
    optparser.add_option('-n', '--size', type=int, default=3)
    optparser.add_option('-k', '--win-size', type=int, default=3)
    optparser.add_option('-1', '--player1', default='Random')
    optparser.add_option('-2', '--player2', default='Random')
    optparser.add_option('-g', '--games', type=int, default=1)

    opts, args = optparser.parse_args()

    board = Board(dimensions=opts.dimensions, size=opts.size, winSize=opts.win_size)

    player1 = makePlayer(opts.player1, 'X')
    player2 = makePlayer(opts.player2, 'O')
    players = [player1, player2]

    play(board, players)

def makePlayer(player, symbol):
    playerClasses = dict(
        Human = Human,
        Random = Random,
    )

    try:
        playerClass = playerClasses[player]
    except KeyError:
        raise ValueError('invalid player type: %s' % player)

    return playerClass(symbol)

def play(board, players):
    print board

    # Take turns infinitely
    turns = itertools.cycle(players)
    for player in turns:
        square = player.chooseMove(board)
        board.apply(player, square)
        print board
        if board.finished():
            break

if __name__ == '__main__':
    main()

