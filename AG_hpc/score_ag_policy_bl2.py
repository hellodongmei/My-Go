import random
import argparse
import os
import numpy as np
from scipy.optimize import minimize

from dlgo import scoring
from dlgo.goboard_fast import GameState
from dlgo.gotypes import Player

def nll_results(ratings, winners, losers):
    all_ratings = np.concatenate([np.ones(1), ratings])
    winner_ratings = all_ratings[winners]
    loser_ratings = all_ratings[losers]
    log_p_wins = np.log(winner_ratings / (winner_ratings + loser_ratings))
    log_likelihood = np.sum(log_p_wins)
    return -1 * log_likelihood

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--score-path','-a', type=dir_path)
    parser.add_argument('--agent-path', '-b', type=dir_path)

    args = parser.parse_args()

    winners = []
    losers = []
    for filename in os.listdir(args.score_path):
        if not filename.endswith('.npy'): continue
        file = os.path.join(args.score_path, filename)
        read_file = np.load(file, allow_pickle=True)
        dict_data = read_file.tolist()

        winners.extend(dict_data['winners'])
        losers.extend(dict_data['losers'])

    agents=[]
    list_agent = os.listdir(args.agent_path)
    list_agent.sort()
    for filename in list_agent:
        # file = os.path.join(args.agent_path, filename)
        agents.append(filename)

    num_agents = len(agents)
    guess = np.ones(num_agents - 1)
    bounds = [(1e-8, None) for _ in guess]
    result = minimize(
        nll_results, guess,
        args=(winners, losers),
        bounds=bounds)
    assert result.success

    abstract_ratings = np.concatenate([np.ones(1), result.x])
    elo_ratings = 400.0 * np.log10(abstract_ratings)
    min_rating = np.min(elo_ratings)
    # Scale so that the weakest player has rating 0
    a = elo_ratings - min_rating

    print(a)
    for filename, rating in zip(agents, a):
        print("%s %.2f" % (filename, rating))
    filename_score = 'score_records_all.npy' 
    np.save(os.path.join(args.score_path, filename_score), a)

if __name__ == '__main__':
    main()
