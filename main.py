#!/usr/bin/env python

import itertools
import optparse
from collections import defaultdict

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
    optparser.add_option('-v', '--verbose', action='store_true')

    opts, args = optparser.parse_args()

    player1 = makePlayer(opts.player1, 'X', 1)
    player2 = makePlayer(opts.player2, 'O', 2)
    players = [player1, player2]

    verbose = opts.verbose
    if any(isinstance(player, Human) for player in players):
        verbose = True

    wins = defaultdict(int)
    for i in xrange(opts.games):
        board = Board(dimensions=opts.dimensions, size=opts.size, winSize=opts.win_size)
        play(board, players, verbose)
        winner = board.winner
        wins[winner] += 1
        if verbose:
            print board
            print 'Game %d -' % (i + 1),
            if winner is None:
                print 'Draw'
            else:
                winningLine = ' '.join(map(str, board.winningLine))
                print '%s won through [ %s ]' % (winner, winningLine)

    for player in players:
        print '%s wins: %d' % (player, wins[player])
    print 'Draws: %d' % wins[None]

def makePlayer(player, symbol, number):
    playerClasses = dict(
        Human = Human,
        Random = Random,
    )

    try:
        playerClass = playerClasses[player]
    except KeyError:
        raise ValueError('invalid player type: %s' % player)

    return playerClass(symbol, number)

def play(board, players, verbose):
    # Take turns infinitely
    turns = itertools.cycle(players)
    for player in turns:
        if verbose:
            print board
        square = player.chooseMove(board)
        board.apply(player, square)
        if board.finished():
            break

if __name__ == '__main__':
    main()

