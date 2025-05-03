from pypokerengine.api.game import setup_config, start_poker
from sample_player.fish_player_setup import FishPlayer
from sample_player.starthand1 import starthand1
from sample_player.ruleplayer import RulePlayer
from sample_player.smart_player import SmartPlayer
from basicRuleBase import ruleBase

# Number of simulations
num_simulations = 100
p2_wins = 0
p3_wins = 0
p4_wins = 0
draw_count = 0

for i in range(num_simulations):
    config = setup_config(max_round=10, initial_stack=100, small_blind_amount=5)
    config.register_player(name="p1", algorithm=SmartPlayer())
    config.register_player(name="p2", algorithm=ruleBase())
    # config.register_player(name="p3", algorithm=starthand1())
    # config.register_player(name="p4", algorithm=RulePlayer())

    game_result = start_poker(config, verbose=0)  # Turn off verbose for speed

    final_stacks = game_result['players']
    winner_names = [p['name'] for p in final_stacks if p['stack'] == max(p['stack'] for p in final_stacks)]

    if len(winner_names) == 2:
        draw_count += 1

    if "p2" in winner_names:
        print("p2 win")
        p2_wins += 1
    # elif "p3" in winner_names:
    #     print("p3 win")
    #     p3_wins += 1
    # elif "p4" in winner_names:
    #     print("p4 win")
    #     p4_wins += 1
    else:
        print("p1 win")

print(f"\nOut of {num_simulations} games, p2 won {p2_wins} times, p3 won {p3_wins}, p4 won {p4_wins}")
print(f"Draw {draw_count} times")
