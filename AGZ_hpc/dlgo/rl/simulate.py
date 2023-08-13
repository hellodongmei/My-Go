# import argparse
# import h5py
from dlgo import scoring
from dlgo import zero
from dlgo.goboard_fast import GameState, Player, Point

def simulate_game(
        board_size,
        black_agent, black_collector,
        white_agent, white_collector):
    print('Starting the game!')
    game = GameState.new_game(board_size)
    agents = {
        Player.black: black_agent,
        Player.white: white_agent,
    }

    black_collector.begin_episode()
    white_collector.begin_episode()
    print('begin_episode')
    while not game.is_over():
        next_move = agents[game.next_player].select_move(game)
        game = game.apply_move(next_move)

    game_result = scoring.compute_game_result(game)
    print(game_result)
    # Give the reward to the right agent.
    if game_result.winner == Player.black:
        black_collector.complete_episode(1)
        white_collector.complete_episode(-1)
    else:
        black_collector.complete_episode(-1)
        white_collector.complete_episode(1)


def experience_simulation(board_size,num_games, black_agent, white_agent):
    collector1 = zero.ZeroExperienceCollector()
    collector2 = zero.ZeroExperienceCollector()
    black_agent.set_collector(collector1)
    white_agent.set_collector(collector2)

    for i in range(num_games):
        simulate_game(board_size, black_agent, collector1, white_agent, collector2)

    return zero.combine_experience([collector1, collector2])