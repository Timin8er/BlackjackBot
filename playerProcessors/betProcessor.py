#!/usr/bin/env python
from PyQt5.QtCore import QThread, pyqtSignal
from util.enums import playerState

# import time
import random

class betProcessor(QThread):

    progress_update = pyqtSignal(int)


    def __init__(self, sim_controller, player_bots : list):
        QThread.__init__(self)
        self.player_bots = player_bots
        self.sim_controller = sim_controller


    def run(self):
        inputs = [0] * 11

        for i in range(len(self.player_bots)):
            player = self.player_bots[i]

            ins = inputs.copy()
            ins.append(player.bet)
            ins.append(player.win_history)
            ins.extend(player.memory)
            ins.append(random.random())

            player.place_bet(ins)
