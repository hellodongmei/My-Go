# tag::alphago_sl_data[]
from dlgo.data.processor import GoDataProcessor
from dlgo.encoders.alphago import AlphaGoEncoder
from dlgo.agent.predict import DeepLearningAgent
from dlgo.networks.alphago import alphago_model

from keras.callbacks import ModelCheckpoint
import h5py

import matplotlib.pyplot as plt
# %matplotlib inline
import numpy as np
import pandas as pd

import os
import argparse

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def main():
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('--num-games', '-a', type=int)
    parser.add_argument('--agent-path','-b', type=dir_path)
    parser.add_argument('--check-path','-c', type=dir_path)
    parser.add_argument('--fig-path','-d', type=dir_path)

    args = parser.parse_args()

    rows, cols = 9, 9
    num_classes = rows * cols
    num_games = args.num_games

    encoder = AlphaGoEncoder()
    processor = GoDataProcessor(encoder=encoder.name())
    print('starting load data')
    generator = processor.load_go_data('train', num_games, use_generator=True)
    test_generator = processor.load_go_data('test', num_games, use_generator=True)
    print('loaded data')
# end::alphago_sl_data[]

# tag::alphago_sl_model[]
    input_shape = (encoder.num_planes, rows, cols)
    alphago_sl_policy = alphago_model(input_shape, is_policy_net=True)

    alphago_sl_policy.compile('sgd', 'categorical_crossentropy', metrics=['accuracy'])
    # set learning rate in optimizer('sgd'), here using default 0.01
# end::alphago_sl_model[]

# print the number of parameter for each layer
    alphago_sl_policy.summary()

# tag::alphago_sl_train[]
    epochs = 3
    batch_size = 128
    hist = alphago_sl_policy.fit(
        generator.generate(batch_size, num_classes),
        epochs=epochs,
        steps_per_epoch=generator.get_num_samples() / batch_size,
        validation_data=test_generator.generate(batch_size, num_classes),
        validation_steps=test_generator.get_num_samples() / batch_size,
        callbacks=[ModelCheckpoint(os.path.join(args.check_path,'alphago_sl_policy_{epoch}.h5'))]
        # callbacks=[ModelCheckpoint('alphago_sl_policy_{epoch}.h5')]
    )
# here, argument 'callbacks' stands for saving checkpoints
    
    pd.DataFrame(hist.history).plot(figsize=(8,5))
    plt.grid(True)
    plt.gca().set_ylim(0, 5)
    plt.title('learning curve')
    plt.savefig(os.path.join(args.fig_path,'image.png'))

    alphago_sl_agent = DeepLearningAgent(alphago_sl_policy, encoder)

    with h5py.File(os.path.join(args.agent_path,'alphago_sl_policy_1.h5'), 'w') as sl_agent_out:
        alphago_sl_agent.serialize(sl_agent_out)
# end::alphago_sl_train[]

    alphago_sl_policy.evaluate(
        test_generator.generate(batch_size, num_classes),
        steps=test_generator.get_num_samples() / batch_size
    )

if __name__=='__main__':
    main()
