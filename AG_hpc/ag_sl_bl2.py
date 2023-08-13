# tag::ag_sl_bl2[]
from dlgo.data.generator import DataGenerator
from dlgo.encoders.alphago import AlphaGoEncoder
from dlgo.agent.predict import DeepLearningAgent
from dlgo.networks.alphago import alphago_model
from tensorflow.keras.callbacks import EarlyStopping
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
    # parser.add_argument('--num-games', '-a', type=int)
    parser.add_argument('--lr', '-b', type=float)
    parser.add_argument('--agent-path','-c', type=dir_path)
    parser.add_argument('--history-path','-d', type=dir_path)
    parser.add_argument('--batchs', '-e', type=int)

    args = parser.parse_args()

    rows, cols = 9, 9
    num_classes = rows * cols

    encoder = AlphaGoEncoder()
    # processor = GoDataProcessor(encoder=encoder.name())
    print('starting load data at %s' % datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    generator = DataGenerator('/home/users/l/liudong1/scratch/AG/data',  'train')
    test_generator = DataGenerator('/home/users/l/liudong1/scratch/AG/data',  'test')
    print('loaded data at %s' % datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
# end::alphago_sl_data[]

# tag::alphago_sl_model[]
    input_shape = (encoder.num_planes, rows, cols)
    alphago_sl_policy = alphago_model(input_shape, is_policy_net=True)

    monitor=EarlyStopping(monitor='val_accuracy', min_delta= 1e-3, patience=5)

    optimizer = keras.optimizers.SGD(learning_rate=args.lr)
    alphago_sl_policy.compile(loss='categorical_crossentropy', optimizer = optimizer, metrics=['accuracy'])
# end::alphago_sl_model[]

# tag::alphago_sl_train[]
    # epochs = 30
    epochs = 30
    batch_size = args.batchs
    train_hist= alphago_sl_policy.fit(
        generator.generate(batch_size, num_classes),
        epochs=epochs,
        steps_per_epoch=generator.get_num_samples() / batch_size,
        validation_data=test_generator.generate(batch_size, num_classes),
        validation_steps=test_generator.get_num_samples() / batch_size,
        callbacks=[monitor]
    )

    # save the training hisotry data
    filename_train_hist = 'train_hist_%.8f_%d.npy' % (args.lr, args.batchs)
    np.save(os.path.join(args.history_path, filename_train_hist), train_hist.history)

    alphago_sl_agent = DeepLearningAgent(alphago_sl_policy, encoder)
    
    filename_policy = 'alphago_sl_policy_%.8f_%d.h5' % (args.lr, args.batchs)
    with h5py.File(os.path.join(args.agent_path,filename_policy), 'w') as sl_agent_out:
        alphago_sl_agent.serialize(sl_agent_out)
# end::alphago_sl_train[]

    test_hist = alphago_sl_policy.evaluate(
        test_generator.generate(batch_size, num_classes),
        steps=test_generator.get_num_samples() / batch_size
    )

    # save the test hisotry data
    filename_test_hist = 'test_hist_%.8f_%d.npy' % (args.lr, args.batchs)
    np.save(os.path.join(args.history_path, filename_test_hist), test_hist)



if __name__=='__main__':
    main()
