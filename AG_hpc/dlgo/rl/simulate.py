from dlgo import rl
from dlgo import scoring
from dlgo import goboard_fast as goboard
from dlgo.gotypes import Player
from dlgo.utils import print_board, print_move
from collections import namedtuple
import time

class GameRecord(namedtuple('GameRecord', 'moves winner margin')):
    pass


def simulate_game(black_player, white_player):
    moves = []
    game = goboard.GameState.new_game(9)
    agents = {
        Player.black: black_player,
        Player.white: white_player,
    }
    print('loaded agents for simulation')
    i=0
    while not game.is_over():
        time.sleep(0.3)
        # print(chr(27) + "[2J")  
        print_board(game.board)
        next_move = agents[game.next_player].select_move(game)
        print_move(game.next_player, next_move)
        moves.append(next_move)
        game = game.apply_move(next_move)
        i+=1
        print('%d step is down' %i)

    game_result = scoring.compute_game_result(game)
    print(game_result)
    time.sleep(3)

    return GameRecord(
        moves=moves,
        winner=game_result.winner,
        margin=game_result.winning_margin,
    )


def experience_simulation(num_games, agent1, agent2):
    collector1 = rl.ExperienceCollector()
    collector2 = rl.ExperienceCollector()

    color1 = Player.black
    for i in range(num_games):
        collector1.begin_episode()
        agent1.set_collector(collector1)
        collector2.begin_episode()
        agent2.set_collector(collector2)

        if color1 == Player.black:
            black_player, white_player = agent1, agent2
        else:
            white_player, black_player = agent2, agent1
        game_record = simulate_game(black_player, white_player)
        if game_record.winner == color1:
            collector1.complete_episode(reward=1)
            collector2.complete_episode(reward=-1)
        else:
            collector2.complete_episode(reward=1)
            collector1.complete_episode(reward=-1)
        color1 = color1.other

    return rl.combine_experience([collector1, collector2])
