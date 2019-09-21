#!/usr/bin/env python
from PyQt5.QtCore import QObject


class dealerBot(QObject):

    def __init__(self, sim_controller, ui_controller):
        QObject.__init__(self)

        self.sim_controller = sim_controller
        self.ui_controller = ui_controller

    def turn(self):
        if self.ui_controller.dealer_total() < 17:
            self.ui_controller.deal_to_dealer()
            return True
        return False

    def run(self):
        while self.turn():
            pass
