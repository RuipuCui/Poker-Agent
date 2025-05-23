import numpy as np
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
import random

NB_SIMULATION = 1000


class SmartHonestPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
            nb_simulation=NB_SIMULATION,
            nb_player=self.nb_player,
            hole_card=gen_cards(hole_card),
            community_card=gen_cards(community_card)
        )

        if win_rate >= 1.6 / self.nb_player and len(valid_actions) == 3:
            roll = np.random.randint(2)
            if roll == 1:
                action = valid_actions[2]  # fetch RAISE action info
            else:
                action = valid_actions[1]   # fetch CALL action info
        elif win_rate >= 1.0 / self.nb_player:
            action = valid_actions[1]   # fetch CALL action info
        else:
            action = valid_actions[0]  # fetch FOLD action info
        
        if action["action"] == "raise":
            amount = random.randint(action["amount"]["min"], action["amount"]["max"])
            if amount == -1: action["action"] = "call"
        else:
            amount = action["amount"]

        return action["action"], amount


    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


class DumbHonestPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
            nb_simulation=NB_SIMULATION,
            nb_player=self.nb_player,
            hole_card=gen_cards(hole_card),
            community_card=gen_cards(community_card)
        )

        if win_rate >= 1.0 / self.nb_player:
            action = valid_actions[1]   # fetch CALL action info
        else:
            action = valid_actions[0]  # fetch FOLD action info
        if action["action"] == "raise":
            amount = action["amount"]["min"]  # Or random between min and max
        else:
            amount = action["amount"]

        if action["action"] == "raise":
            amount = random.randint(action["amount"]["min"], action["amount"]["max"])
            if amount == -1: action["action"] = "call"
        else:
            amount = action["amount"]
            
        return action["action"], amount

    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


class ConversativeHonestPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
            nb_simulation=NB_SIMULATION,
            nb_player=self.nb_player,
            hole_card=gen_cards(hole_card),
            community_card=gen_cards(community_card)
        )

        if win_rate >= 1.8 / self.nb_player and len(valid_actions) == 3:
            action = valid_actions[2]  # fetch RAISE action info
        elif win_rate >= 1.1 / self.nb_player and len(valid_actions) == 3:
            roll = np.random.randint(3)
            if roll == 0:
                action = valid_actions[2]  # fetch RAISE action info
            else:
                action = valid_actions[1]   # fetch CALL action info
        elif win_rate >= 0.8 / self.nb_player:
            action = valid_actions[1]   # fetch CALL action info
        else:
            action = valid_actions[0]  # fetch FOLD action info
            
        if action["action"] == "raise":
            amount = action["amount"]["min"]  # Or random between min and max
        else:
            amount = action["amount"]

        if action["action"] == "raise":
            amount = random.randint(action["amount"]["min"], action["amount"]["max"])
            if amount == -1: action["action"] = "call"
        else:
            amount = action["amount"]
            
        return action["action"], amount

    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass