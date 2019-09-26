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

            if player.game_state == playerState.In:
                if player.hit_or_hold() == playerState.In:
                    self.remaing_in += 1

            self.progress_update.emit(i+1)

            # if i == 5:
            #     print ([
            #         player.board_controller.player_total(),
            #         player.board_controller.dealer_total()
            #     ])
            # if i % 10 == 0:
            #     print (player.hit_or_hold())

            # time.sleep(0.05)
