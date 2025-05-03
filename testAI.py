from pypokerengine.api.game import setup_config, start_poker
from sample_player.fish_player_setup import FishPlayer
#from basicRuleBase import SmartHonestPlayer, DumbHonestPlayer, ConversativeHonestPlayer
from basicRuleBase import ruleBase
from HonstPlayer import SmartHonestPlayer, DumbHonestPlayer, ConversativeHonestPlayer
from QLearning import QLearningPlayer
from submission.mybot import MyBot

# Number of simulations
num_simulations = 100
p1_wins = 0
p3_wins = 0

for i in range(num_simulations):
    config = setup_config(max_round=10, initial_stack=100, small_blind_amount=5)
    config.register_player(name="p2", algorithm=SmartHonestPlayer())
    config.register_player(name="p3", algorithm=MyBot())
    # config.register_player(name="p5", algorithm=deepLearningPlayer(load_weights=True))
    # config.register_player(name="p2", algorithm=ruleBase())
    game_result = start_poker(config, verbose=0)  # Turn off verbose for speed

    final_stacks = game_result['players']
    winner_names = [p['name'] for p in final_stacks if p['stack'] == max(p['stack'] for p in final_stacks)]

    if "p3" in winner_names:
        p3_wins += 1
    
    if "p1" in winner_names:
        p1_wins += 1

    print(str(winner_names))

print(f"\nOut of {num_simulations} games, p3 won {p3_wins} times.")
print(f"\nOut of {num_simulations} games, p3 won {p1_wins} times.")
