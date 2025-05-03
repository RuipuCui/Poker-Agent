# train_model.py
from pypokerengine.api.game import setup_config, start_poker
from deepLearning import deepLearningPlayer
from sample_player.fish_player_setup import FishPlayer
from basicRuleBase import ruleBase
from sample_player.smart_player import SmartPlayer
from HonstPlayer import SmartHonestPlayer

train_bot = deepLearningPlayer(load_weights=False)

for i in range(1000):  # You can raise this number
    print(f"Training game {i+1}")
    config = setup_config(max_round=10, initial_stack=1000, small_blind_amount=5)
    config.register_player(name="p1", algorithm=train_bot)
    config.register_player(name="p2", algorithm=ruleBase())
    config.register_player(name="p3", algorithm=FishPlayer())
    config.register_player(name="p4", algorithm=SmartPlayer())
    config.register_player(name="p5", algorithm=SmartHonestPlayer())

    start_poker(config, verbose=0)

train_bot.save_weights()
