from __future__ import print_function
# tag::bot_vs_bot[]
from dlgo import goboard_fast as goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move
import time
from dlgo.agent import load_prediction_agent, load_policy_agent, AlphaGoMCTS,RandomBot
from dlgo.agent import TerminationAgent
from dlgo.rl import load_value_agent
from dlgo import scoring
import h5py
from dlgo import zero


def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)

    #fast_policy = load_prediction_agent(h5py.File('/home/users/l/liudong1/scratch/compare/agents/ag_fast.h5', 'r'))
    strong_policy = load_policy_agent(h5py.File('/home/users/l/liudong1/scratch/compare/agents/ag_rl_policy_0.h5', 'r'))
    # fast_policy = load_prediction_agent(h5py.File('./agents/alphago_sl_policy_test_opti.h5', 'r'))
    # strong_policy = load_policy_agent(h5py.File('./agents/alphago_sl_policy_test_opti.h5', 'r'))
    #value = load_value_agent(h5py.File('/home/users/l/liudong1/scratch/compare/agents/valphago_value_1.h5', 'r'))

   # alphago = AlphaGoMCTS(strong_policy, fast_policy, value)
   # bot1 = TerminationAgent(alphago)
    # AGAGZ = zero.load_prediction_agent(h5py.File('./agents/ag_agz.h5','r'))
    # AGAGZ.set_paras(20,2)
    # bot2 = AGAGZ
    bot1 = strong_policy
    bot2 = strong_policy

    bots = {
        gotypes.Player.black: bot1,
        gotypes.Player.white: bot2,
    }
    while not game.is_over():
        time.sleep(0.3)  # <1>

        # print(chr(27) + "[2J")  # <2>
        print_board(game.board)
        bot_move = bots[game.next_player].select_move(game)
        print_move(game.next_player, bot_move)
        game = game.apply_move(bot_move)

    game_result = scoring.compute_game_result(game)
    print(game_result.winner)
    print(game_result.winning_margin)


if __name__ == '__main__':
    main()

# <1> We set a sleep timer to 0.3 seconds so that bot moves aren't printed too fast to observe
# <2> Before each move we clear the screen. This way the board is always printed to the same position on the command line.
# end::bot_vs_bot[]
