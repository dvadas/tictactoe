#!/usr/bin/env python

import itertools
import optparse
from collections import defaultdict

from players import Player, Human, Random, Centre
from board import Board, Square

VERBOSE_FINAL_RESULTS, VERBOSE_GAME_END, VERBOSE_MOVE, VERBOSE_HUMAN = range(4)
def main():
    optparser = optparse.OptionParser('usage: %prog [options]')
    optparser.add_option('-d', '--dimensions', type=int, default=2)
    optparser.add_option('-n', '--size', type=int, default=3)
    optparser.add_option('-k', '--win-size', type=int, default=3)
    optparser.add_option('-1', '--player1', default='Random')
    optparser.add_option('-2', '--player2', default='Random')
    optparser.add_option('-g', '--games', type=int, default=1)
    optparser.add_option('-v', '--verbose', action='count', default=0)

    opts, args = optparser.parse_args()

    player1 = makePlayer(opts.player1, 'X', 1)
    player2 = makePlayer(opts.player2, 'O', 2)
    players = [player1, player2]

    verbose = opts.verbose
    if any(isinstance(player, Human) for player in players):
        verbose = VERBOSE_HUMAN

    wins = defaultdict(int)
    for i in xrange(opts.games):
        board = Board(dimensions=opts.dimensions, size=opts.size, winSize=opts.win_size)
        play(board, players, verbose)
        winner = board.winner
        wins[winner] += 1
        if verbose >= VERBOSE_GAME_END:
            if verbose >= VERBOSE_HUMAN:
                print board.humanReadableStr() + '\n'
            else:
                print board
            print 'Game %d -' % (i + 1),
            if winner is None:
                print 'Draw'
            else:
                winningLine = ' '.join(map(str, board.winningLine))
                print '%s won through [ %s ]' % (winner, winningLine)

        players.reverse()

    if verbose >= VERBOSE_FINAL_RESULTS:
        for player in players:
            print '%s wins: %d' % (player, wins[player])
        print 'Draws: %d' % wins[None]

def makePlayer(player, symbol, number):
    playerClasses = dict(
        Human = Human,
        Random = Random,
        Centre = Centre,
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
        if verbose >= VERBOSE_HUMAN:
            print board.humanReadableStr() + '\n'
        elif verbose >= VERBOSE_MOVE:
            print board
        square = player.chooseMove(board)
        board.apply(player, square)
        if board.finished():
            break

if __name__ == '__main__':
    main()

