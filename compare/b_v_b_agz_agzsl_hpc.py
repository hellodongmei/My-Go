# tag::bot_vs_bot[]
from __future__ import print_function
from dlgo import goboard_fast as goboard
from dlgo.goboard_fast import GameState
from dlgo import gotypes
from dlgo.utils import print_board, print_move
import time
import argparse
import random
import numpy as np
import h5py
import os

from dlgo import scoring
from dlgo.gotypes import Player
from dlgo import zero

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def simulate_game(black_player, white_player, board_size):
    # moves = []
    game = GameState.new_game(board_size)
    agents = {
        Player.black: black_player,
        Player.white: white_player,
    }
    while not game.is_over():
        print_board(game.board)
        next_move = agents[game.next_player].select_move(game)
        print_move(game.next_player, next_move)
        # moves.append(next_move)
        game = game.apply_move(next_move)

    game_result = scoring.compute_game_result(game)

    return game_result.winner

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-games', '-a', type=int)
    parser.add_argument('--gpu-number', '-b', type=int)
    parser.add_argument('--rounds-move', '-c', type=int)
    parser.add_argument('--exp-path','-d', type=dir_path)
    parser.add_argument('agents', nargs='+')

    args = parser.parse_args()

    num_games = args.num_games

    agents = [
        zero.load_prediction_agent(h5py.File(filename))
        for filename in args.agents]

    for a in agents:
        a.set_paras(args.rounds_move,2)

    num_agents = len(agents)
    agent_ids = list(range(num_agents))

    winners = np.zeros(num_games, dtype=np.int32)
    losers = np.zeros(num_games, dtype=np.int32)

    for i in range(num_games):
        print("Game %d / %d..." % (i + 1, num_games))
        black_id, white_id = random.sample(agent_ids, 2)
        winner = simulate_game(agents[black_id], agents[white_id], 9)
        print("Winner is : %s" % (winner))
        print("black:", black_id) 
        print("white:", white_id)

        if winner == Player.black:
            winners[i] = black_id
            losers[i] = white_id
        else:
            winners[i] = white_id
            losers[i] = black_id

    result_dict = {}
    winners = winners.tolist()
    losers = losers.tolist()
    result_dict['winners'] = winners
    result_dict['losers'] = losers
    print(result_dict)
    filename_score = 'score_records_%d.npy' % args.gpu_number
    np.save(os.path.join(args.score_path, filename_score), result_dict)



if __name__ == '__main__':
    main()

# <1> We set a sleep timer to 0.3 seconds so that bot moves aren't printed too fast to observe
# <2> Before each move we clear the screen. This way the board is always printed to the same position on the command line.
# end::bot_vs_bot[]

