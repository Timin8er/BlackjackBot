#!/usr/bin/env python
from PyQt5.QtCore import QObject
from util.enums import playerState

import random

class playerBot(QObject):

    def __init__(self, board_controller, parent_bot = None):
        QObject.__init__(self)

        self.board_controller = board_controller

        self.money = 50
        self.fitness = 0
        self.games_won = 0
        self.games_lost = 0
        self.games_played = 0
        self.card_total = 0

        self.reset()

        # randomize from parent
        if parent_bot:
            self.threshold = parent_bot.threshold + random.random() - 0.5
        # completely random
        else:
            self.threshold = random.random() * 21



    def reset(self):
        self.card_total = 0
        self.game_state = playerState.In


    def hit_or_hold(self):
        if self.game_state == playerState.In:
            self.card_total = self.board_controller.player_total()
            if self.card_total > self.threshold:
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
        self.fitness = self.games_won / self.games_played
