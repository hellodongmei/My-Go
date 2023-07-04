# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import print_function
from __future__ import absolute_import
import os
import random
from six.moves import range


class Sampler:
    """Sample training and test data from zipped sgf files such that test data is kept stable."""
    def __init__(self, data_dir='data', num_test_games=100, cap_month=11, seed=1337):
        self.data_dir = data_dir
        self.num_test_games = num_test_games
        self.test_games = []
        self.train_games = []
        self.test_folder = 'test_samples.py'
        self.cap_month = cap_month

        random.seed(seed)
        self.compute_test_samples()

    def draw_data(self, data_type, num_samples):
        if data_type == 'test':
            return self.test_games
        elif data_type == 'train' and num_samples is not None:
            return self.draw_training_samples(num_samples)
        elif data_type == 'train' and num_samples is None:
            return self.draw_all_training()
        else:
            raise ValueError(data_type + " is not a valid data type, choose from 'train' or 'test'")

    def draw_samples(self, num_sample_games):
        """Draw num_sample_games many training games from index."""
        available_games = []
        index = os.listdir(self.data_dir)

        for filename in index:
            if not filename.endswith('.sgf'): continue
            month = int(filename.split('-')[1])
            if month > self.cap_month:
                continue
            available_games.append(filename) 
        print('>>> Total number of games used: ' + str(len(available_games)))

        sample_set = set()
        while len(sample_set) < num_sample_games:
            sample = random.choice(available_games)
            if sample not in sample_set:
                sample_set.add(sample)
        print('Drawn ' + str(num_sample_games) + ' samples:')
        return list(sample_set)

    def draw_training_games(self):
        """Get list of all non-test games, that are no later than dec 2014
        Ignore games after cap_year to keep training data stable
        """
        index = os.listdir(self.data_dir)
        for filename in index:
            if not filename.endswith('.sgf'): continue
            month = int(filename.split('-')[1])
            if month > self.cap_month:
                continue
            sample = filename
            if sample not in self.test_games:
                self.train_games.append(sample)            
        print('total num training games: ' + str(len(self.train_games)))

    def compute_test_samples(self):
        """If not already existing, create local file to store fixed set of test samples"""
        if not os.path.isfile(self.test_folder):
            test_games = self.draw_samples(self.num_test_games)
            test_sample_file = open(self.test_folder, 'w')
            for sample in test_games:
                test_sample_file.write(str(sample) + "\n")
            test_sample_file.close()

        test_sample_file = open(self.test_folder, 'r')
        sample_contents = test_sample_file.read()
        test_sample_file.close()
        # for filename in sample_contents:
        #     self.test_games.append(filename)
        for line in sample_contents.split('\n'):
            if line != "":
                # (filename, index) = eval(line)
                self.test_games.append(line)



    def draw_training_samples(self, num_sample_games):
        """Draw training games, not overlapping with any of the test games."""
        available_games = []
        index = os.listdir(self.data_dir)
        for filename in index:
            if not filename.endswith('.sgf'): continue
            month = int(filename.split('-')[1])
            if month > self.cap_month:
                continue
            available_games.append(filename)
        print('total num games: ' + str(len(available_games)))

        sample_set = set()
        while len(sample_set) < num_sample_games:
            sample = random.choice(available_games)
            if sample not in self.test_games:
                sample_set.add(sample)
        print('Drawn ' + str(num_sample_games) + ' samples:')
        return list(sample_set)        



    def draw_all_training(self):
        """Draw all available training games."""
        available_games = []
        index = os.listdir(self.data_dir)

        for filename in index:
            if not filename.endswith('.sgf'): continue
            month = int(filename.split('-')[1])
            if month > self.cap_month:
                continue
            available_games.append(filename)
            # num_games = len(index)
            # for i in range(num_games):
            #     available_games.append((filename, i))
        print('total num games: ' + str(len(available_games)))

        sample_set = set()
        for sample in available_games:
            if sample not in self.test_games:
                sample_set.add(sample)
        print('Drawn all samples, ie ' + str(len(sample_set)) + ' samples:')
        return list(sample_set)
