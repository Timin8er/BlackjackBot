import random

class deckController:

    _deck = [
        {'rank':0,  'suit':0, 'value':11, 'in_play':0},
        {'rank':1,  'suit':0, 'value':2,  'in_play':0},
        {'rank':2,  'suit':0, 'value':3,  'in_play':0},
        {'rank':3,  'suit':0, 'value':4,  'in_play':0},
        {'rank':4,  'suit':0, 'value':5,  'in_play':0},
        {'rank':5,  'suit':0, 'value':6,  'in_play':0},
        {'rank':6,  'suit':0, 'value':7,  'in_play':0},
        {'rank':7,  'suit':0, 'value':8,  'in_play':0},
        {'rank':8,  'suit':0, 'value':9,  'in_play':0},
        {'rank':9,  'suit':0, 'value':10, 'in_play':0},
        {'rank':10, 'suit':0, 'value':10, 'in_play':0},
        {'rank':11, 'suit':0, 'value':10, 'in_play':0},
        {'rank':12, 'suit':0, 'value':10, 'in_play':0},
        {'rank':0,  'suit':1, 'value':11, 'in_play':0},
        {'rank':1,  'suit':1, 'value':2,  'in_play':0},
        {'rank':2,  'suit':1, 'value':3,  'in_play':0},
        {'rank':3,  'suit':1, 'value':4,  'in_play':0},
        {'rank':4,  'suit':1, 'value':5,  'in_play':0},
        {'rank':5,  'suit':1, 'value':6,  'in_play':0},
        {'rank':6,  'suit':1, 'value':7,  'in_play':0},
        {'rank':7,  'suit':1, 'value':8,  'in_play':0},
        {'rank':8,  'suit':1, 'value':9,  'in_play':0},
        {'rank':9,  'suit':1, 'value':10, 'in_play':0},
        {'rank':10, 'suit':1, 'value':10, 'in_play':0},
        {'rank':11, 'suit':1, 'value':10, 'in_play':0},
        {'rank':12, 'suit':1, 'value':10, 'in_play':0},
        {'rank':0,  'suit':2, 'value':11, 'in_play':0},
        {'rank':1,  'suit':2, 'value':2,  'in_play':0},
        {'rank':2,  'suit':2, 'value':3,  'in_play':0},
        {'rank':3,  'suit':2, 'value':4,  'in_play':0},
        {'rank':4,  'suit':2, 'value':5,  'in_play':0},
        {'rank':5,  'suit':2, 'value':6,  'in_play':0},
        {'rank':6,  'suit':2, 'value':7,  'in_play':0},
        {'rank':7,  'suit':2, 'value':8,  'in_play':0},
        {'rank':8,  'suit':2, 'value':9,  'in_play':0},
        {'rank':9,  'suit':2, 'value':10, 'in_play':0},
        {'rank':10, 'suit':2, 'value':10, 'in_play':0},
        {'rank':11, 'suit':2, 'value':10, 'in_play':0},
        {'rank':12, 'suit':2, 'value':10, 'in_play':0},
        {'rank':0,  'suit':3, 'value':11, 'in_play':0},
        {'rank':1,  'suit':3, 'value':2,  'in_play':0},
        {'rank':2,  'suit':3, 'value':3,  'in_play':0},
        {'rank':3,  'suit':3, 'value':4,  'in_play':0},
        {'rank':4,  'suit':3, 'value':5,  'in_play':0},
        {'rank':5,  'suit':3, 'value':6,  'in_play':0},
        {'rank':6,  'suit':3, 'value':7,  'in_play':0},
        {'rank':7,  'suit':3, 'value':8,  'in_play':0},
        {'rank':8,  'suit':3, 'value':9,  'in_play':0},
        {'rank':9,  'suit':3, 'value':10, 'in_play':0},
        {'rank':10, 'suit':3, 'value':10, 'in_play':0},
        {'rank':11, 'suit':3, 'value':10, 'in_play':0},
        {'rank':12, 'suit':3, 'value':10, 'in_play':0}
    ]

    def __init__(self, game_ui):
        self.game_ui = game_ui
        self.n_decks = 5
        self.deck_progress = 0
        self.total_cards = self.n_decks*52
        self.deck_min = 18

        self.dealer_cards = []
        self.player_cards = []

        self.dealer_total = 0
        self.player_total = 0

        self._bot_inputs = [0]*21
        # 0-9 : player cards shorthand
        # 10 : dealer card shorthand
        # 11 - 20

    def reset(self):
        self._bot_inputs = [0]*21
        self.dealer_total = 0
        self.player_total = 0
        self.deck_progress = 0
        for c in self._deck:
            c['in_play'] = 0


    def clear_board(self):
        self.dealer_total = 0
        self.player_total = 0
        self.dealer_cards = []
        self.player_cards = []

        for i in range(11):
            self._bot_inputs[i] = 0

        if self.will_shuffle():
            self.shuffle_deck()


    def will_shuffle(self):
        if self.deck_progress > self.total_cards - self.deck_min:
            return True
        else:
            return False


    def shuffle_deck(self):
        for c in self._deck:
            c['in_play'] = 0
        self.deck_progress = 0


    def inputs(self):
        return self._bot_inputs


    def card_total(self, cards):
        sum = 0
        for c in cards:
            sum += c['value']

        for c in cards:
            if c['value'] == 11 and sum > 21:
                sum -= 10
        return sum


    def get_random_card(self):
        return self._deck[random.randint(0,51)]


    def deal_random_unplayed_card(self):
        card = None
        while True:
            card = self.get_random_card()
            if card['in_play'] < self.n_decks:
                break
        card['in_play'] += 1
        self._bot_inputs[card['value'] + 9] += 1
        self.deck_progress += 1
        return card


    def deal_to_dealer(self):
        new_card = self.deal_random_unplayed_card()
        self.dealer_cards.append(new_card)
        self.dealer_total = self.card_total(self.dealer_cards)
        self._bot_inputs[10] = self.dealer_total
        # self.game_ui.deal_to_dealer(new_card)
        return new_card


    def deal_to_player(self):
        new_card = self.deal_random_unplayed_card()
        self.player_cards.append(new_card)
        self.player_total = self.card_total(self.player_cards)
        self._bot_inputs[new_card['value'] - 2] += 1
        # self.game_ui.deal_to_player(new_card)
        return new_card
