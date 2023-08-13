# tag::ag_sl_bl1[]
from dlgo.data.processor import GoDataProcessor
from dlgo import zero

import argparse


def main():
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('--num-games', '-a', type=int)

    args = parser.parse_args()

    num_games = args.num_games
    test_games=2036
   # test_games=45

    board_size = 9
    encoder = zero.ZeroEncoder(board_size)
    processor = GoDataProcessor(encoder=encoder.name())
    print('starting load data')
    processor.load_go_data('train', num_games, test_games, use_generator=True)
    processor.load_go_data('test', num_games, test_games, use_generator=True)

if __name__=='__main__':
    main()
