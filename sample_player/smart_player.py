import random
from pypokerengine.players import BasePokerPlayer
from sample_player.starthand1 import starthand1
from sample_player.fish_player_setup import FishPlayer
from sample_player.ruleplayer import RulePlayer

class SmartPlayer(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hole_card, round_state):
        street = round_state['street']
        if street == "preflop":
            action, amount = starthand1().declare_action(valid_actions, hole_card, round_state)
        else:
            action, amount = RulePlayer().declare_action(valid_actions, hole_card, round_state)
        return action, amount   # action returned here is sent to the poker engine

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return SmartPlayer()
