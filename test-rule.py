from pypokerengine.api.game import setup_config, start_poker
from sample_player.fish_player_setup import FishPlayer
from sample_player.random_player_setup import RandomPlayer
from sample_player.starthand1 import starthand1
from basicRuleBase import SmartHonestPlayer, DumbHonestPlayer, ConversativeHonestPlayer
from sample_player.ruleplayer import RulePlayer

# Number of simulations
num_simulations = 100
p5_wins = 0

for i in range(num_simulations):
    config = setup_config(max_round=10, initial_stack=100, small_blind_amount=5)
    # config.register_player(name="p1", algorithm=FishPlayer())
    # config.register_player(name="p2", algorithm=RandomPlayer())
    config.register_player(name="p3", algorithm=starthand1())

    config.register_player(name="p5", algorithm=RulePlayer())

    game_result = start_poker(config, verbose=0)  # Turn off verbose for speed

    final_stacks = game_result['players']
    winner_names = [p['name'] for p in final_stacks if p['stack'] == max(p['stack'] for p in final_stacks)]

    if "p5" in winner_names:
        p5_wins += 1

    print(str(winner_names))

print(f"\nOut of {num_simulations} games, p5 won {p5_wins} times.")
