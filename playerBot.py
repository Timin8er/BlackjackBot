#!/usr/bin/env python
from PyQt5.QtCore import QObject
from util.enums import playerState

from nuralNetLayer import nuralNetLayer

import random
import numpy

class playerBot(QObject):

    def __init__(self, board_controller, parent_bot = None):
        QObject.__init__(self)

        self.board_controller = board_controller

        self.money = 100
        self.fitness = 0
        self.games_won = 0
        self.games_lost = 0
        self.games_played = 0
        self.card_total = 0
        self.nural_net = None

        self.reset()

        if parent_bot:
            self.nural_net = nuralNetLayer(parent = parent_bot.nural_net)


    def reset(self):
        self.card_total = 0
        self.game_state = playerState.In


    def hit_or_hold(self):
        self.card_total = self.board_controller.player_total()

        r = self.nural_net.feedforward([
            self.card_total,
            self.board_controller.dealer_total()
        ])

        if r[0] > 0.5:
            self.game_state = playerState.In
        else:
            self.game_state = playerState.Out
        return self.game_state


    def win_game(self):
        self.games_played += 1
        self.games_won += 1
        self.money += 1

        self.recalc_fitness()


    def lose_game(self):
        self.games_played += 1
        self.games_lost += 1
        self.money -= 1

        self.recalc_fitness()


    def tie_game(self):
        self.games_played += 1

        self.recalc_fitness()


    def recalc_fitness(self):
        self.fitness = self.games_won
        # self.fitness = self.games_won / self.games_played

    def sigma(self, x):
        return 1 / (1 + numpy.exp(-x))
