# tag::ag_sl_bl2[]
from dlgo.data.generator import DataGenerator

from tensorflow.keras.layers import Activation, BatchNormalization, Conv2D, Dense, Flatten, Input
from tensorflow.keras.models import Model

from dlgo.rl.simulate import experience_simulation
from dlgo.data.processor import GoDataProcessor
from dlgo import zero

from tensorflow import keras
import h5py

import numpy as np
import pandas as pd

import os
import argparse
from datetime import datetime

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def main():
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('--lr', '-b', type=float)
    parser.add_argument('--agent-path','-c', type=dir_path)
    parser.add_argument('--history-path','-d', type=dir_path)
    parser.add_argument('--batchs', '-e', type=int)

    args = parser.parse_args()

    board_size = 9
    num_classes = board_size * board_size

    encoder = zero.ZeroEncoder(board_size)
    # processor = GoDataProcessor(encoder=encoder.name())
    print('starting load data at %s' % datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    generator = DataGenerator('/home/users/l/liudong1/scratch/AG_AGZ/data',  'train')
    test_generator = DataGenerator('/home/users/l/liudong1/scratch/AG_AGZ/data',  'test')
    print('loaded data at %s' % datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
# end::alphago_sl_data[]

# tag::alphago_sl_model[]
    board_input = Input(shape=encoder.shape(), name='board_input')
    pb = board_input

    for i in range(4):
        pb = Conv2D(64, (3, 3),
            padding='same',
            data_format='channels_first')(pb)
        pb = BatchNormalization(axis=1)(pb)
        pb = Activation('relu')(pb)

    # Policy output
    policy_conv = Conv2D(2, (1, 1), data_format='channels_first')(pb)
    policy_batch = BatchNormalization(axis=1)(policy_conv)
    policy_relu = Activation('relu')(policy_batch)
    policy_flat = Flatten()(policy_relu)
    policy_output = Dense(encoder.num_moves(), activation='softmax')(
        policy_flat)

    # Value output
    value_conv = Conv2D(1, (1, 1), data_format='channels_first')(pb)
    value_batch = BatchNormalization(axis=1)(value_conv)
    value_relu = Activation('relu')(value_batch)
    value_flat = Flatten()(value_relu)
    value_hidden = Dense(256, activation='relu')(value_flat)
    value_output = Dense(1, activation='tanh')(value_hidden)

    ag_agz = Model(
        inputs=[board_input],
        outputs=[policy_output, value_output])
    # model.compile('sgd', 'categorical_crossentropy', metrics=['accuracy'])

    # monitor=EarlyStopping(monitor='val_accuracy', min_delta= 1e-3, patience=5)

    optimizer = keras.optimizers.SGD(learning_rate=args.lr)
    # agz_mcts_sl_policy.compile(loss='categorical_crossentropy', optimizer = optimizer, metrics=['accuracy'])
    ag_agz.compile(
            optimizer = optimizer,
            loss=['categorical_crossentropy', 'mse'])
# end::alphago_sl_model[]

# tag::alphago_sl_train[]
    #epochs = 30
    epochs = 150
    batch_size = args.batchs
    train_hist= ag_agz.fit(
        generator.generate(batch_size, num_classes),
        epochs=epochs,
        steps_per_epoch=generator.get_num_samples() / batch_size,
        validation_data=test_generator.generate(batch_size, num_classes),
        validation_steps=test_generator.get_num_samples() / batch_size
        # callbacks=[monitor]
    )

    # save the training hisotry data
    filename_train_hist = 'train_hist_%.8f_%d.npy' % (args.lr, args.batchs)
    np.save(os.path.join(args.history_path, filename_train_hist), train_hist.history)

    alphago_sl_agent = zero.ZeroAgent(ag_agz, encoder)
    
    filename_policy = 'alphago_sl_policy_%.8f_%s.h5' % (args.lr, args.batchs)
    print(filename_policy)
    # with h5py.File(os.path.join(args.agent_path,filename_policy)) as sl_agent_out:
    #     alphago_sl_agent.serialize(sl_agent_out)
    # alphago_sl_agent.serialize(filename_policy)
    alphago_sl_agent.serialize(os.path.join(args.agent_path, filename_policy))
# # end::alphago_sl_train[]



if __name__=='__main__':
    main()

