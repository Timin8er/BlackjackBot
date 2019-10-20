#!/usr/bin/env python
# from PyQt5.QtCore import QObject
from util.enums import playerState

from nuralNetLayer import nuralNetLayer

import math
import random
import numpy

class playerBot(object):

    def __init__(self, parent_bot = None):
        # QObject.__init__(self)
        self.hh_nural_net = None
        self.eg_nural_net = None
        self.age = -1

        self.bet = 1
        self.insurence = 0

        self.reset()

        if parent_bot:
            self.hh_nural_net = nuralNetLayer(parent = parent_bot.hh_nural_net)
            self.eg_nural_net = nuralNetLayer(parent = parent_bot.eg_nural_net)


    def reset(self):
        self.active = True
        self.money = 500
        self.memory = [0]*10
        self.games_won = 0
        self.games_lost = 0
        self.games_played = 0
        self.fitness = 0
        self.age += 1
        self.new_game_reset()


    def new_game_reset(self):
        self.my_cards = [0,0,0,0,0,0,0,0,0,0]
        self.card_total = 0
        self.game_state = playerState.In


    def tally_my_cards(self, cards):
        """
        Use the given card array to sum my cards.
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
        return self.hh_nural_net.feed_forward(inputs)


    def hit_or_hold_feed(self, input_cards, insurence_available = False):
        """
        inputs is an array of 10 player cards and 1 dealer card
        """
        if self.active:

            inputs = input_cards.copy()
            inputs.append(self.bet)
            inputs.extend(self.memory)
            inputs.append(random.random())
            r = self.hh_nural_net.feed_forward(inputs)

            # the first output determines weather the bot will request a hit (in) or hold (out)
            if r[0] > 0.5:
                self.game_state = playerState.In
            else:
                self.game_state = playerState.Out
                # if we're out, tally our total
                self.my_cards = self.tally_my_cards(input_cards[0:10])

            if insurence_available:
                # the second output is the bots insurence bet
                b = r[1]
                # un-sigmoid the output
                self.insurence = int(max(math.log((1/b)-1), 0))
            return self.game_state
        else:
            self.game_state = playerState.Out
            return self.game_state



    def end_game_feed(self, all_cards : list, wlt : int, shuffle : bool, ):
        if self.active:
            inputs = all_cards.copy()
            inputs.append(wlt)
            inputs.append(shuffle)
            inputs.append(self.bet)
            inputs.extend(self.memory)
            inputs.append(random.random())
            r = self.eg_nural_net.feed_forward(inputs)

            # first 10 outputs are for memory adjustments
            # next 10 outputs are for memory reset
            for i in range(10):
                self.memory[i] = numpy.clip(self.memory[i] + r[i], -20, 20)
                if r[i+10]:
                    self.memory[i] = 0

            # last output is bet
            if self.money > 1:
                self.bet = numpy.clip(int(r[20]), 1, self.money)
            else:
                self.bet = 0
                self.active = False
            return self.bet
        else:
            return 0


    def win_game(self):
        if self.active:
            self.games_played += 1
            self.games_won += 1
            self.money += self.bet

            self.recalc_fitness()


    def lose_game(self):
        if self.active:
            self.games_played += 1
            self.games_lost += 1
            self.money -= self.bet

            self.recalc_fitness()


    def tie_game(self):
        if self.active:
            self.games_played += 1

            self.recalc_fitness()


    def recalc_fitness(self):
        self.fitness = self.money
        # self.fitness = self.games_won / self.games_played


    def force_death(self):
        self.active = False
        self.fitness = 0


    def to_dict(self):
        data = {}
        data['hh'] = []
        n = self.hh_nural_net
        while n:
            data['hh'].append(n.weights)
            data['hh'].append(n.biases)
            n = n.next_layer

        data['endgame'] = []
        n = self.eg_nural_net
        while n:
            data['endgame'].append(n.weights)
            data['endgame'].append(n.biases)
            n = n.next_layer

        return data


    def build_from_dict(self, data:dict):
        index = 0 # index of the data we loaded
        layer = self.hh_nural_net # current layer,
        net_hh = data['hh']
        while index < len(net_hh): # iterate throught the loaded data
            if index != 0: # create a new layer if not on the first one
                layer = layer.add_layer()

            # give the layer its weights and biases
            layer.weights = net_hh[index]
            layer.biases = net_hh[index+1]
            index += 2

    # with open('grandfatherMemoryNuralNet.json') as nf:
    #     net = json.loads(nf.read())

        index = 0 # index of the data we loaded
        layer = self.eg_nural_net # current layer
        net_eg = data['endgame']
        while index < len(net_eg): # iterate throught the loaded data
            if index != 0: # create a new layer if not on the first one
                layer = layer.add_layer()

            # give the layer its weights and biases
            layer.weights = net_eg[index]
            layer.biases = net_eg[index+1]
            layer.use_sigma = False
            index += 2
