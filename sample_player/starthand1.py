from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards
import random

class starthand1(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hole_card, round_state):

        # SUIT_MAP = {2 :'C', 4 :'D', 8 :'H', 16:'S'}
        
        # Default action: fold
        action, amount = valid_actions[0]['action'], valid_actions[0]['amount']
        street = round_state['street']        

        # starting hand
        if street == "preflop":
            hand = gen_cards(hole_card)

            rank_hi = max(hand[0].rank, hand[1].rank)
            rank_lo = min(hand[0].rank, hand[1].rank)
            # suit1 = SUIT_MAP[hand[0].suit]
            # suit2 = SUIT_MAP[hand[1].suit]
            suit1 = hand[0].suit
            suit2 = hand[1].suit
            
            if rank_hi == 14 or (rank_hi == 13 and rank_lo > 4) or (rank_hi == 12 and rank_lo > 7):
                # raise if possible
                action_info = valid_actions[2]
                action, amount = action_info['action'], random.randint(action_info["amount"]["min"], action_info["amount"]["max"])
                if amount == -1: action = "call"
                return action, amount

            if rank_hi == 13 or (rank_hi == 12 and rank_lo > 5) or (rank_hi == 11 and rank_lo > 7):
                # only raise if same suit else call
                if suit1 == suit2:
                    action_info = valid_actions[2]
                    action, amount = action_info['action'], random.randint(action_info["amount"]["min"], action_info["amount"]["max"])
                    if amount == -1: action = "call"
                else:
                    action_info = valid_actions[1]
                    action, amount = action_info['action'], action_info["amount"]
                return action, amount
        else:
            # call if not first round
            call_action_info = valid_actions[1]
            action, amount = call_action_info["action"], call_action_info["amount"]
    
        return action, amount   # otherwise fold

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
    return starthand1()
