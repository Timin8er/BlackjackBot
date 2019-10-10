#!/usr/bin/env python
from PyQt5.QtCore import QObject


class dealerBot(QObject):

    def __init__(self, sim_controller, deck_controller):
        QObject.__init__(self)

        self.sim_controller = sim_controller
        self.deck_controller = deck_controller

    def hithold(self):
        return (self.deck_controller.dealer_total < 17)
