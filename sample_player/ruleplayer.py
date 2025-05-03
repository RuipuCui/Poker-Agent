from collections import Counter
import random
from pypokerengine.players import BasePokerPlayer

class RulePlayer(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

    def estimate_hand_strength(self, hole_cards, community_cards, street):
        """
        Returns: "very_strong", "strong", "decent", or "weak"
        """
        all_cards = hole_cards + community_cards
        ranks = [card[0] for card in all_cards]  # e.g., 'A', 'K', '2'
        suits = [card[1] for card in all_cards]  # e.g., 's', 'h'

        rank_counter = Counter(ranks)
        suit_counter = Counter(suits)

        def has_pair():
            return any(c == 2 for c in rank_counter.values())

        def has_two_pair():
            return len([r for r in rank_counter.values() if r == 2]) >= 2

        def has_three_of_a_kind():
            return any(c == 3 for c in rank_counter.values())

        def has_flush():
            return any(c >= 5 for c in suit_counter.values())

        def has_full_house():
            return has_three_of_a_kind() and has_pair()

        def has_four_of_a_kind():
            return any(c == 4 for c in rank_counter.values())

        # Simplified logic based on street
        if has_four_of_a_kind() or has_full_house() or has_flush():
            return "very_strong"

        if has_three_of_a_kind() or has_two_pair():
            return "strong"

        if has_pair():
            return "decent"

        # Preflop-specific logic
        if street == "preflop":
            high_cards = ['A', 'K', 'Q', 'J']
            card_ranks = [c[0] for c in hole_cards]
            if card_ranks[0] == card_ranks[1]:  # Pocket pair
                if card_ranks[0] in high_cards:
                    return "strong"
                else:
                    return "decent"
            elif all(r in high_cards for r in card_ranks):
                return "decent"

        return "weak"


    def get_action_info(self, valid_actions, action_name):
        for action in valid_actions:
            if action["action"] == action_name:
                return action
        return None

    def fold(self, valid_actions):
        action_info = self.get_action_info(valid_actions, "fold")
        return "fold", action_info["amount"]

    def call(self, valid_actions):
        action_info = self.get_action_info(valid_actions, "call")
        return "call", action_info["amount"]


    def raise_action(self, valid_actions):
        raise_info = self.get_action_info(valid_actions, "raise")
        if raise_info is None:
            return self.call(valid_actions)  # fallback if raise not allowed

        min_amount = raise_info["amount"]["min"]
        max_amount = raise_info["amount"]["max"]

        # Edge case: invalid range
        if min_amount == -1 or max_amount == -1 or min_amount > max_amount:
            return self.call(valid_actions)

        amount = random.randint(min_amount, max_amount)
        return "raise", amount


    def declare_action(self, valid_actions, hole_card, round_state):
        
        community_card = round_state['community_card']                  
        street = round_state['street']
        action_histories = round_state['action_histories']

        # 1st round: (1) estimate card strength (2) fold / call
        # 2nd round: (1) re-estimate card strength (2) see other player's actions. if they raise, and we don't have amazing, fold. if they check, keep checking
        # 3rd round: (1) re-estimate card strength (2) see other player's actions. if they raise, and we don't have amazing, fold. if they check, keep checking
        # 4th round: (1) re-estimate card strength (2) see other player's actions. if they raise, and we don't have amazing, fold. if they check, keep checking

        def can_raise():
            return self.get_action_info(valid_actions, "raise") is not None

        estimate = self.estimate_hand_strength(hole_card, community_card, street)
        opponent_raised = any(action['action'] == 'raise' for action in action_histories[street])

        if street == 'preflop':
            if (estimate == "strong" or estimate == "very_strong") and can_raise():
                return self.raise_action(valid_actions)
            elif estimate == "weak":
                return self.call(valid_actions)
            else:
                return self.call(valid_actions)

        else:  # flop / turn / river
            if (estimate == "strong" or estimate == "very_strong") and can_raise():
                return self.raise_action(valid_actions)
            elif opponent_raised:
                if estimate in ["decent", "strong", "very_strong"]:
                    return self.call(valid_actions)
                else:
                    return self.fold(valid_actions)
            else:
                return self.call(valid_actions) 


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
    return RulePlayer()
