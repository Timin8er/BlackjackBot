#!/usr/bin/env python
from PyQt5.QtCore import QObject


class dealerBot(QObject):

    def __init__(self, board_controller):
        QObject.__init__(self)

        self.board_controller = board_controller

    def turn(self):
        if self.board_controller.dealer_total() < 17:
            self.board_controller.deal_to_dealer()
            return True
        return False

    def run(self):
        while self.turn():
            pass
