import argparse
import os
import h5py
from tensorflow.keras.layers import Activation, BatchNormalization, Conv2D, Dense, Flatten, Input
from tensorflow.keras.models import Model

from dlgo.rl.simulate import experience_simulation
from dlgo import zero

import numpy as np

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def main():

    # Create two agents from the model and encoder.
    # 10 is a very small value for rounds_per_move. To train a strong
    # bot, you should run at least a few hundred rounds per move.
    
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('--sim-num-games', '-a', type=int)
    parser.add_argument('--rounds-per-move','-b',  type=int)
    parser.add_argument('--exp-path','-c', type=dir_path)
    parser.add_argument('--exp-id','-d',  type=int)
    parser.add_argument('agents', nargs='+')

    args = parser.parse_args()
    
    # load agents and set parameters
    agents = [
        zero.load_prediction_agent(h5py.File(filename))
        for filename in args.agents]

    c=2.0
    for a in agents:
        a.set_paras(args.rounds_per_move, c)

    board_size = 9
    
    for i in range(args.sim_num_games):
        experience = experience_simulation(board_size, 1, agents[0], agents[1])
        filename = 'exp_%d_%d.h5' % (args.exp_id, i+1)
        with h5py.File(os.path.join(args.exp_path, filename), 'w') as exp_f:
            experience.serialize(exp_f)

    # simulate self-play games and save them to npy file
    # experience = experience_simulation(board_size, args.sim_num_games, agents[0], agents[1])
    # # exp_path = args.exp_path
    # # np.save(os.path.join(args.exp_path, 'exp_states_{}.npy'.format(int(args.exp_id))), 
    # # 	experience.states)
    # # np.save(os.path.join(args.exp_path, 'exp_visit_counts_{}.npy'.format(int(args.exp_id))), 
    # # 	experience.visit_counts)
    # # np.save(os.path.join(args.exp_path,'exp_rewards_{}.npy'.format(int(args.exp_id))), 
    # # 	experience.rewards)
    # with h5py.File(os.path.join(args.exp_path,'exp_{}.h5'.format(int(args.exp_id))), 'w') as exp_f:
    #     experience.serialize(exp_f)
    # experience.serialize(os.path.join(args.exp_path,'exp_{}.h5'.format(int(args.exp_id))))

if __name__ == '__main__':
    main()

    
