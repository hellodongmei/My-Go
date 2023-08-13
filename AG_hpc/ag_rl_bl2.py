import argparse
import os
import h5py
import numpy as np

from dlgo.rl.simulate import experience_simulation
from dlgo.rl.experience import combine_experience,load_experience
from dlgo.agent.predict import load_prediction_agent
from dlgo.agent.pg import PolicyAgent, load_policy_agent
from dlgo.encoders.alphago import AlphaGoEncoder
from dlgo import elo


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def main():

    # Combine all parallel simulated experience
    
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('--exp-path','-b', type=dir_path)
    parser.add_argument('--model-path','-c', type=dir_path)
    parser.add_argument('--model-id','-d',  type=int)
    parser.add_argument('black_agent')

    args = parser.parse_args()
    

    load_exps = []
    for filename in os.listdir(args.exp_path):
        if not filename.endswith('.h5'): continue
        file = os.path.join(args.exp_path, filename)
        load_exp = load_experience(h5py.File(file))
        load_exps.append(load_exp)
        # experience.join_l(load_exp)
    experience = combine_experience(load_exps)

    encoder = AlphaGoEncoder()
    agent = load_prediction_agent(h5py.File(args.black_agent))
    black_agent = PolicyAgent(agent.model, encoder)
    pre_agent = PolicyAgent(agent.model, encoder)

    black_agent.train(experience)
    
    # calculate elo score
    agents = [black_agent, pre_agent]
    ratings = elo.calculate_ratings(agents, 1000, 9)
    if ratings[0] - ratings[1] <= 0:
        raise Exception('need more training experience')

    with h5py.File(os.path.join(args.model_path, "rl_policy_{}.h5".format(int(args.model_id))), 'w') as black_agent_out:
        black_agent.serialize(black_agent_out)

if __name__ == '__main__':
    main()
