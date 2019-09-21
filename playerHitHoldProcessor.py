#!/usr/bin/env python
from PyQt5.QtCore import QThread, pyqtSignal
from util.enums import playerState

import time

class playerHitHoldProcessor(QThread):

    progress_update = pyqtSignal(int)


    def __init__(self, player_bots : list):
        QThread.__init__(self)
        self.player_bots = player_bots

        self.update_tempo = 10
        self.remaing_in = 100



    def run(self):
        self.remaing_in = 0
        for i in range(len(self.player_bots)):
            player = self.player_bots[i]

            if player.hit_or_hold() == playerState.In:
                self.remaing_in += 1

            self.progress_update.emit(i+1)

            # time.sleep(0.05)
