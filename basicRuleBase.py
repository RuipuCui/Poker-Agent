import random
from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

class ruleBase(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']

        action, amount = valid_actions[1]['action'], valid_actions[1]['amount']

        if len(community_card) != 0:
            winrate = estimate_hole_card_win_rate(
                nb_simulation=1000,
                nb_player=3,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
            )
            #print("Winrate:", winrate)

            if winrate > 0.8 and valid_actions[0]['action'] == 'raise':
                # Raise if winrate is high
                raise_info = valid_actions[0]['amount']
                amount = random.randint(raise_info['min'], raise_info['max'])
                action = 'raise'
            elif winrate <= 0.5 and valid_actions[2]['action'] == 'fold':
                # Fold if winrate is low
                action = 'fold'
                amount = 0
            else:
                # Otherwise call
                action, amount = valid_actions[1]['action'], valid_actions[1]['amount']
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


