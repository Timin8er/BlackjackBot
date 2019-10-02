#!/usr/bin/env python
from PyQt5.QtCore import QThread, pyqtSignal
from util.enums import playerState

import time

class playerHitHoldProcessor(QThread):

    progress_update = pyqtSignal(int)


    def __init__(self, sim_controller, player_bots : list):
        QThread.__init__(self)
        self.player_bots = player_bots
        self.sim_controller = sim_controller

        self.update_tempo = 10
        self.remaing_in = 100



    def run(self):
        inputs = self.sim_controller.game_ui._player_cards_input.copy()
        inputs.append(self.sim_controller.game_ui._dealer_total)

        self.remaing_in = 0
        for i in range(len(self.player_bots)):
            player = self.player_bots[i]

            if player.game_state == playerState.In:
                if player.hit_or_hold(inputs) == playerState.In:
                    self.remaing_in += 1

            self.progress_update.emit(i+1)

            # time.sleep(0.05)
