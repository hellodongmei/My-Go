import argparse
import os
import h5py
import numpy as np

from dlgo import agent
from dlgo import elo
from dlgo import rl

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-games', '-g', type=int)
    parser.add_argument('--board-size', '-b', type=int)
    parser.add_argument('--agent-id', '-c', type=int)
    parser.add_argument('--score-path','-d', type=dir_path)
    parser.add_argument('agents', nargs='+')

    args = parser.parse_args()

    agents = [
        agent.load_policy_agent(h5py.File(filename))
        # rl.load_q_agent(h5py.File(filename))
        for filename in args.agents]
    for a in agents:
        a.set_temperature(0.02)

    ratings = elo.calculate_ratings(agents, args.num_games, args.board_size)

    data = []

    for filename, rating in zip(args.agents, ratings):
        print("%s %.2f" % (filename, rating))
        data.append((filename, rating))

    
    filename_score = 'filename_score_%d.npy' % args.agent_id
    np.save(os.path.join(args.score_path, filename_score), data)


if __name__ == '__main__':
    main()
