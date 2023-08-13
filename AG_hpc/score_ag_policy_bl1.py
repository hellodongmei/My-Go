import argparse
import random
import numpy as np
import h5py
import os

from dlgo import agent
from dlgo import rl
from dlgo import scoring
from dlgo.goboard_fast import GameState
from dlgo.gotypes import Player

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def simulate_game(black_player, white_player, board_size):
    moves = []
    game = GameState.new_game(board_size)
    agents = {
        Player.black: black_player,
        Player.white: white_player,
    }
    while not game.is_over():
        next_move = agents[game.next_player].select_move(game)
        moves.append(next_move)
        game = game.apply_move(next_move)

    game_result = scoring.compute_game_result(game)

    return game_result.winner



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-games', '-a', type=int)
    parser.add_argument('--gpu-number', '-b', type=int)
    # parser.add_argument('--rounds-move', '-c', type=int)
    parser.add_argument('--score-path','-d', type=dir_path)
    parser.add_argument('--agents','-e', type=dir_path)
    # parser.add_argument('agents', nargs='+')

    args = parser.parse_args()
    
    agents=[]
    num_games = args.num_games
    list_agent = os.listdir(args.agents)
    list_agent.sort()
    for filename in list_agent:
        print(filename)
        file = os.path.join(args.agents, filename)
        #print(filename)
        agent_i = agent.load_policy_agent(h5py.File(file,'r'))
        agents.append(agent_i)


    # agents = [
    #     zero.load_prediction_agent(h5py.File(filename))
    #     # rl.load_q_agent(h5py.File(filename))
    #     for filename in args.agents]
    # for a in agents:
    #     a.set_paras(args.rounds_move,2)

    num_agents = len(agents)
    agent_ids = list(range(num_agents))

    winners = np.zeros(num_games, dtype=np.int32)
    losers = np.zeros(num_games, dtype=np.int32)

    for i in range(num_games):
        print("Game %d / %d..." % (i + 1, num_games))
        black_id, white_id = random.sample(agent_ids, 2)
        winner = simulate_game(agents[black_id], agents[white_id], 9)
        print("Winner is : %s" % (winner))
        if winner == Player.black:
            winners[i] = black_id
            losers[i] = white_id
        else:
            winners[i] = white_id
            losers[i] = black_id
    
    # save the result
    result_dict = {}
    winners = winners.tolist()
    losers = losers.tolist()
    result_dict['winners'] = winners
    result_dict['losers'] = losers
    filename_score = 'score_records_%d.npy' % args.gpu_number
    np.save(os.path.join(args.score_path, filename_score), result_dict)


if __name__ == '__main__':
    main()

