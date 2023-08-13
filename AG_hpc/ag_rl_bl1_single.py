import argparse
import os
import h5py
from dlgo.agent.pg import PolicyAgent
from dlgo.agent.predict import load_prediction_agent
from dlgo.encoders.alphago import AlphaGoEncoder
from dlgo.rl.simulate import experience_simulation

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
    parser.add_argument('--num-games', '-a', type=int)
    parser.add_argument('--exp-path','-b', type=dir_path)
    parser.add_argument('--exp-id','-c',  type=int)
    parser.add_argument('--temp','-d',  type=int)
    parser.add_argument('agents', nargs='+')

    args = parser.parse_args()
    
    # load agents and set parameters
    agents_dl = [
        load_prediction_agent(h5py.File(filename)) # return a deeplearning agent
        for filename in args.agents]
    
    encoder = AlphaGoEncoder()
    agents = [PolicyAgent(agent_dl.model, encoder) for agent_dl in agents_dl]
    
    temperature = args.temp
    for a in agents:
        a.set_temperature(temperature)

    board_size = 9
    
    # simulate self-play games and save them to npy file
    for i in range(args.num_games):
        experience = experience_simulation(1, agents[0], agents[1])
        with h5py.File(os.path.join(args.exp_path,'exp_{}_{}.h5'.format(int(args.exp_id)), i+1), 'w') as exp_f:
            experience.serialize(exp_f)
    # experience = experience_simulation(args.num_games, agents[0], agents[1])
    # with h5py.File(os.path.join(args.exp_path,'exp_{}.h5'.format(int(args.exp_id))), 'w') as exp_f:
    #     experience.serialize(exp_f)

if __name__ == '__main__':
    main()