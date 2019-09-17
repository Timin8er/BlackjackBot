#!/usr/bin/env python
from PyQt5.QtCore import QObject
from util.enums import playerState


class playerBot(QObject):

    def __init__(self, board_controller):
        QObject.__init__(self)

        self.board_controller = board_controller

        self.money = 10
        self.fitness = 0
        self.games_won = 0
        self.games_lost = 0
        self.games_played = 0

        self.reset()


    def reset(self):
        self.card_total = 0
        self.game_state = playerState.In


    def hit_or_hold(self):
        if self.game_state == playerState.In:
            self.card_total = self.board_controller.player_total()
            if self.card_total > 16:
                self.game_state = playerState.Out
        return self.game_state


    def win_game(self):
        self.games_played += 1
        self.games_won += 1
        self.money += 1

        self.fitness = self.games_won / self.games_lost


    def lose_game(self):
        self.games_played += 1
        self.games_lost += 1
        self.money -= 1

        self.fitness = self.games_won / self.games_lost
