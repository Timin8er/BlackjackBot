#!/usr/bin/env python
from PyQt5.QtCore import QThread
from playerProcessors.playerProcessor import playerProcessor

import random

class betProcessor(playerProcessor):

    def run(self):
        self.inputs = [0] * 11
        playerProcessor.run(self)


    def operation(self, bot):
        ins = self.inputs.copy()
        ins.append(bot.bet)
        ins.append(bot.win_history)
        ins.extend(bot.memory)
        ins.append(random.random())

        bot.place_bet(ins)
