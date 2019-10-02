#!/usr/bin/env python
from PyQt5.QtCore import QObject
from util.enums import playerState

from nuralNetLayer import nuralNetLayer

import random
import numpy
import math

class playerBot(QObject):

    def __init__(self, board_controller, parent_bot = None):
        QObject.__init__(self)

        self.board_controller = board_controller

        self.card_total = 0
        self.nural_net = None

        self.bet = 1
        self.win_history = 0
        self.memory = [0,0,0,0,0,0,0,0,0,0]

        self.reset()

        if parent_bot:
            self.nural_net = nuralNetLayer(parent = parent_bot.nural_net)

        self.original = False


    def reset(self):
        self.card_total = 0
        self.money = 100
        self.games_won = 0
        self.games_lost = 0
        self.games_played = 0
        self.fitness = 0
        self.new_game_reset()


    def new_game_reset(self):
        self.card_total = 0
        self.game_state = playerState.In


    def feed_forward(self, inputs):
        return self.nural_net.feed_forward(inputs)


    def hit_or_hold(self, inputs):
        r = self.feed_forward(inputs)

        if r[0] > 0.5:
            self.game_state = playerState.In
        else:
            self.game_state = playerState.Out
            self.card_total = self.board_controller.player_total()
        return self.game_state


    def place_bet(self, inputs):
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

    def sigma(self, x):
        return 1 / (1 + numpy.exp(-x))
