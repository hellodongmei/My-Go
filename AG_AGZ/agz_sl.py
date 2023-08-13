import argparse
import h5py
from tensorflow.keras.layers import Activation, BatchNormalization, Conv2D, Dense, Flatten, Input
from tensorflow.keras.models import Model

from dlgo.rl.simulate import experience_simulation
from dlgo.data.processor import GoDataProcessor
from dlgo import zero
from dlgo import elo

import numpy as np

def main:
	board_size = 9
	encoder = zero.ZeroEncoder(board_size)
	num_games = 30
	test_games=25

	processor = GoDataProcessor(encoder=encoder.name())
	generator = processor.load_go_data('train', num_games, test_games, use_generator=True)

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
	value_relu = Activation('relu')(value_batch)
	value_flat = Flatten()(value_relu)
	value_hidden = Dense(256, activation='relu')(value_flat)
	value_output = Dense(1, activation='tanh')(value_hidden)

	model = Model(
    	inputs=[board_input],
    	outputs=[policy_output, value_output])
	model.compile('sgd', 'categorical_crossentropy', metrics=['accuracy'])

	epochs = 1
	batch_size = 128
	train_hist= model.fit(
    	generator.generate(batch_size, num_classes),
    	epochs=epochs,
    	steps_per_epoch=generator.get_num_samples() / batch_size,
    	validation_data=test_generator.generate(batch_size, num_classes),
    	validation_steps=test_generator.get_num_samples() / batch_size
    	)

	# solve the generator is empty