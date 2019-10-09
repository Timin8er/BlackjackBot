#!/usr/bin/env python
# from PyQt5.QtCore import QObject
from util.enums import playerState

from nuralNetLayer import nuralNetLayer

import math
import random

class playerBot(object):

    def __init__(self, parent_bot = None):
        # QObject.__init__(self)
        self.nural_net = None

        self.bet = 1
        self.win_history = 0
        self.memory = [0,0,0,0,0,0,0,0,0,0]

        self.reset()

        if parent_bot:
            self.nural_net = nuralNetLayer(parent = parent_bot.nural_net)


    def reset(self):
        self.money = 100
        self.games_won = 0
        self.games_lost = 0
        self.games_played = 0
        self.fitness = 0
        self.new_game_reset()


    def new_game_reset(self):
        self.my_cards = [0,0,0,0,0,0,0,0,0,0]
        self.card_total = 0
        self.game_state = playerState.In


    def set_cards(self, cards):
        """
        use the given card array to sum my cards
        """
        self.card_total = 0
        self.card_total += cards[0]*3
        self.card_total += cards[1]*4
        self.card_total += cards[2]*5
        self.card_total += cards[3]*6
        self.card_total += cards[4]*2
        self.card_total += cards[5]*7
        self.card_total += cards[6]*8
        self.card_total += cards[7]*9
        self.card_total += cards[8]*10
        self.card_total += cards[9]*11
        n_aces = cards[9]

        while self.card_total > 21 and n_aces:
            self.card_total -= 10
            n_aces -= 1


    def get_card_total(self):
        return self.card_total


    def feed_forward(self, inputs):
        return self.nural_net.feed_forward(inputs)


    def hit_or_hold(self, input_cards):
        """
        inputs is an array of 10 player cards and 1 dealer card
        """
        imputs = inputs.copy()
        inputs.append(self.bet)
        inputs.append(self.win_history)
        inputs.extend(self.memory)
        inputs.append(random.random())
        r = self.feed_forward(inputs)

        if r[0] > 0.5:
            self.game_state = playerState.In
        else:
            self.game_state = playerState.Out
            self.my_cards = self.set_cards(input_cards[0:10])
        return self.game_state


    def place_bet(self, inputs):
        inputs = [0] * 11
        inputs.append(self.bet)
        inputs.append(self.win_history)
        inputs.extend(self.memory)
        inputs.append(random.random())
        r = self.feed_forward(inputs)

        b = r[1]
        self.bet = max(math.log((1/b)-1), 1)
        return self.bet


    def win_game(self):
        self.games_played += 1
        self.games_won += 1
        self.money += self.bet

        if self.win_history:
            self.win_history += 1
        else:
            self.win_history = 1

        self.recalc_fitness()


    def lose_game(self):
        self.games_played += 1
        self.games_lost += 1
        self.money -= self.bet

        if self.win_history:
            self.win_history = -1
        else:
            self.win_history -= 1

        self.recalc_fitness()


    def tie_game(self):
        self.games_played += 1

        self.recalc_fitness()


    def recalc_fitness(self):
        self.fitness = self.money
        # self.fitness = self.games_won / self.games_played
