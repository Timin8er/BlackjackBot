#!/usr/bin/env python
from PyQt5.QtCore import QThread, pyqtSignal
from util.enums import playerState


class playerHitHoldProcessor(QThread):

    progress_update = pyqtSignal(int)


    def __init__(self, player_bots : list):
        QThread.__init__(self)
        self.player_bots = player_bots

        self.update_tempo = 10
        self.has_remaing_In = True



    def run(self):
        self.has_remaing_In = False
        for i in range(len(self.player_bots)):
            player = self.player_bots[i]

            if player.hit_or_hold() == playerState.In:
                self.has_remaing_In = True

            self.progress_update.emit(i+1)
