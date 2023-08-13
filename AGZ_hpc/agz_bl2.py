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
        load_exp = zero.load_experience(h5py.File(file))
        load_exps.append(load_exp)
        # experience.join_l(load_exp)
    experience = zero.combine_experience(load_exps)

    black_agent = zero.load_prediction_agent(h5py.File(args.black_agent))

    black_agent.train(experience, 0.01, 2048)
    black_agent.serialize(os.path.join(args.model_path, "agent_zero_{}.h5".format(int(args.model_id))))

if __name__ == '__main__':
    main()
