#!/usr/bin/env python
from PyQt5.QtCore import pyqtSignal
from util.enums import playerState
from playerProcessors.playerProcessor import playerProcessor

import random

class hitHoldProcessor(playerProcessor):

    progress_update = pyqtSignal(int)


    def __init__(self, sim_controller, player_bots : list):
        playerProcessor.__init__(self, sim_controller, player_bots)

        self.update_tempo = 10
        self.remaing_in = 100


    def run(self):
        self.inputs = self.sim_controller.game_ui._player_cards_input.copy()
        self.inputs.append(self.sim_controller.game_ui._dealer_total)

        self.remaing_in = 0

        playerProcessor.run(self)


    def operation(self, bot):

        ins = self.inputs.copy()
        ins.append(bot.bet)
        ins.append(bot.win_history)
        ins.extend(bot.memory)
        ins.append(random.random())

        if bot.game_state == playerState.In:
            if bot.hit_or_hold(ins) == playerState.In:
                self.remaing_in += 1
