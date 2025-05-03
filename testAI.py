from pypokerengine.api.game import setup_config, start_poker
from sample_player.fish_player_setup import FishPlayer
#from basicRuleBase import SmartHonestPlayer, DumbHonestPlayer, ConversativeHonestPlayer
from deepLearning import deepLearningPlayer
from basicRuleBase import ruleBase
from HonstPlayer import SmartHonestPlayer, DumbHonestPlayer, ConversativeHonestPlayer
from QLearning import QLearningPlayer

# Number of simulations
num_simulations = 100
p2_wins = 0

for i in range(num_simulations):
    config = setup_config(max_round=10, initial_stack=100, small_blind_amount=5)
    config.register_player(name="p1", algorithm=FishPlayer())
    config.register_player(name="p2", algorithm=SmartHonestPlayer())
    config.register_player(name="p3", algorithm=QLearningPlayer())
    # config.register_player(name="p5", algorithm=deepLearningPlayer(load_weights=True))
    # config.register_player(name="p2", algorithm=ruleBase())
    game_result = start_poker(config, verbose=0)  # Turn off verbose for speed

    final_stacks = game_result['players']
    winner_names = [p['name'] for p in final_stacks if p['stack'] == max(p['stack'] for p in final_stacks)]

    if "p3" in winner_names:
        p2_wins += 1

    print(str(winner_names))

print(f"\nOut of {num_simulations} games, p2 won {p2_wins} times.")
