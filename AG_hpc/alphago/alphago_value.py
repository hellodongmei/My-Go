# tag::init_value[]
from dlgo.networks.alphago import alphago_model
from dlgo.encoders.alphago import AlphaGoEncoder
from dlgo.rl import ValueAgent
from dlgo.rl.experience import combine_experience,load_experience

import argparse
import os
import h5py
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
    parser.add_argument('--value-path','-c', type=dir_path)
    parser.add_argument('--value-id','-d',  type=int)

    args = parser.parse_args()
    
    load_exps = []
    for filename in os.listdir(args.exp_path):
        if not filename.endswith('.h5'): continue
        file = os.path.join(args.exp_path, filename)
        load_exp = load_experience(h5py.File(file))
        load_exps.append(load_exp)
        # experience.join_l(load_exp)
    experience = combine_experience(load_exps)

    rows, cols = 9, 9
    encoder = AlphaGoEncoder()
    input_shape = (encoder.num_planes, rows, cols)
    alphago_value_network = alphago_model(input_shape)

    alphago_value = ValueAgent(alphago_value_network, encoder)
# end::init_value[]

# tag::train_value[]

    alphago_value.train(experience)

    with h5py.File(os.path.join(args.value_path, "valphago_value_{}.h5".format(int(args.value_id))), 'w') as value_agent_out:
        alphago_value.serialize(value_agent_out)
# end::train_value[]

if __name__=='__main__':
    main()