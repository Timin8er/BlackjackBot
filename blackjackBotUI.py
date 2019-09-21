#!/usr/bin/env python
import sys
import random
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, QRect

from simulationController import simulationController

from blackjackBotMainWindow import Ui_MainWindow


class blackjackBotUI(QMainWindow, Ui_MainWindow):

    deck = [
        {'object':None, 'rank':0,  'suit':0, 'value':11,  'in_play':False},
        {'object':None, 'rank':1,  'suit':0, 'value':2,  'in_play':False},
        {'object':None, 'rank':2,  'suit':0, 'value':3,  'in_play':False},
        {'object':None, 'rank':3,  'suit':0, 'value':4,  'in_play':False},
        {'object':None, 'rank':4,  'suit':0, 'value':5,  'in_play':False},
        {'object':None, 'rank':5,  'suit':0, 'value':6,  'in_play':False},
        {'object':None, 'rank':6,  'suit':0, 'value':7,  'in_play':False},
        {'object':None, 'rank':7,  'suit':0, 'value':8,  'in_play':False},
        {'object':None, 'rank':8,  'suit':0, 'value':9,  'in_play':False},
        {'object':None, 'rank':9,  'suit':0, 'value':10, 'in_play':False},
        {'object':None, 'rank':10, 'suit':0, 'value':10, 'in_play':False},
        {'object':None, 'rank':11, 'suit':0, 'value':10, 'in_play':False},
        {'object':None, 'rank':12, 'suit':0, 'value':10, 'in_play':False},
        {'object':None, 'rank':0,  'suit':1, 'value':11,  'in_play':False},
        {'object':None, 'rank':1,  'suit':1, 'value':2,  'in_play':False},
        {'object':None, 'rank':2,  'suit':1, 'value':3,  'in_play':False},
        {'object':None, 'rank':3,  'suit':1, 'value':4,  'in_play':False},
        {'object':None, 'rank':4,  'suit':1, 'value':5,  'in_play':False},
        {'object':None, 'rank':5,  'suit':1, 'value':6,  'in_play':False},
        {'object':None, 'rank':6,  'suit':1, 'value':7,  'in_play':False},
        {'object':None, 'rank':7,  'suit':1, 'value':8,  'in_play':False},
        {'object':None, 'rank':8,  'suit':1, 'value':9,  'in_play':False},
        {'object':None, 'rank':9,  'suit':1, 'value':10, 'in_play':False},
        {'object':None, 'rank':10, 'suit':1, 'value':10, 'in_play':False},
        {'object':None, 'rank':11, 'suit':1, 'value':10, 'in_play':False},
        {'object':None, 'rank':12, 'suit':1, 'value':10, 'in_play':False},
        {'object':None, 'rank':0,  'suit':2, 'value':11,  'in_play':False},
        {'object':None, 'rank':1,  'suit':2, 'value':2,  'in_play':False},
        {'object':None, 'rank':2,  'suit':2, 'value':3,  'in_play':False},
        {'object':None, 'rank':3,  'suit':2, 'value':4,  'in_play':False},
        {'object':None, 'rank':4,  'suit':2, 'value':5,  'in_play':False},
        {'object':None, 'rank':5,  'suit':2, 'value':6,  'in_play':False},
        {'object':None, 'rank':6,  'suit':2, 'value':7,  'in_play':False},
        {'object':None, 'rank':7,  'suit':2, 'value':8,  'in_play':False},
        {'object':None, 'rank':8,  'suit':2, 'value':9,  'in_play':False},
        {'object':None, 'rank':9,  'suit':2, 'value':10, 'in_play':False},
        {'object':None, 'rank':10, 'suit':2, 'value':10, 'in_play':False},
        {'object':None, 'rank':11, 'suit':2, 'value':10, 'in_play':False},
        {'object':None, 'rank':12, 'suit':2, 'value':10, 'in_play':False},
        {'object':None, 'rank':0,  'suit':3, 'value':11,  'in_play':False},
        {'object':None, 'rank':1,  'suit':3, 'value':2,  'in_play':False},
        {'object':None, 'rank':2,  'suit':3, 'value':3,  'in_play':False},
        {'object':None, 'rank':3,  'suit':3, 'value':4,  'in_play':False},
        {'object':None, 'rank':4,  'suit':3, 'value':5,  'in_play':False},
        {'object':None, 'rank':5,  'suit':3, 'value':6,  'in_play':False},
        {'object':None, 'rank':6,  'suit':3, 'value':7,  'in_play':False},
        {'object':None, 'rank':7,  'suit':3, 'value':8,  'in_play':False},
        {'object':None, 'rank':8,  'suit':3, 'value':9,  'in_play':False},
        {'object':None, 'rank':9,  'suit':3, 'value':10, 'in_play':False},
        {'object':None, 'rank':10, 'suit':3, 'value':10, 'in_play':False},
        {'object':None, 'rank':11, 'suit':3, 'value':10, 'in_play':False},
        {'object':None, 'rank':12, 'suit':3, 'value':10, 'in_play':False},
    ]


    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.show()

        self.simulation_controller = simulationController(self)
        self.total_bots = self.simulation_controller.player_bots

        # controll button icons
        self.btn_pause.setIcon(QIcon('icons/pause.png'))
        self.btn_step.setIcon(QIcon('icons/skip-forward.png'))
        self.btn_step_round.setIcon(QIcon('icons/double-skip-forward.png'))
        self.btn_play.setIcon(QIcon('icons/play.png'))

        # controll button functions
        self.btn_pause.clicked.connect(self.action_pause)
        self.btn_pause.clicked.connect(self.simulation_controller.action_pause)
        self.btn_play.clicked.connect(self.action_play)
        self.btn_play.clicked.connect(self.simulation_controller.action_play)
        self.btn_step_round.clicked.connect(self.action_step_game)
        self.btn_step_round.clicked.connect(self.simulation_controller.action_step_game)
        self.btn_step.clicked.connect(self.action_step)
        self.btn_step.clicked.connect(self.simulation_controller.action_step)

        self.btn_pause.setEnabled(False)

        self._cards_sheet = QPixmap('icons/cards.png')
        self._cards_w = self._cards_sheet.width() / 13
        self._cards_h = self._cards_sheet.height() / 4

        self._dealer_cards = []
        self._player_cards = []

        self._dealer_total = 0
        self._player_total = 0





    # ==========================================================================
    # actions for controlling the simulation

    def action_pause(self):
        self.btn_pause.setEnabled(False)
        self.btn_step.setEnabled(True)
        self.btn_step_round.setEnabled(True)
        self.btn_play.setEnabled(True)


    def action_step(self):
        self.btn_pause.setEnabled(True)
        self.btn_step.setEnabled(False)
        self.btn_step_round.setEnabled(True)
        self.btn_play.setEnabled(True)


    def action_step_game(self):
        self.btn_pause.setEnabled(True)
        self.btn_step.setEnabled(True)
        self.btn_step_round.setEnabled(False)
        self.btn_play.setEnabled(True)


    def action_play(self):
        self.btn_pause.setEnabled(True)
        self.btn_step.setEnabled(True)
        self.btn_step_round.setEnabled(True)
        self.btn_play.setEnabled(False)



    # ==========================================================================
    # actions for controlling the playspace
    def clear_board(self):
        self.progressBar.setProperty("value", 0)

        for i in self._dealer_cards:
            i['object'].deleteLater()
        for i in self._player_cards:
            i['object'].deleteLater()

        self._dealer_cards = []
        self._player_cards = []
        self._dealer_total = 0
        self._player_total = 0

        for i in self.deck:
            i['in_play'] = False


    def get_random_card(self):
        return self.deck[random.randint(0,51)]


    def get_random_unplayed_card(self):
        card = None
        while True:
            card = self.get_random_card()
            if card['in_play'] == False:
                break
        return card


    def generate_card_widget(self, card : dict):
        label = QLabel()
        pixmap = self._cards_sheet.copy(QRect(
            card['rank'] * self._cards_w,
            card['suit'] * self._cards_h,
            self._cards_w,
            self._cards_h))

        label.setPixmap(pixmap)

        card['object'] = label
        # print (card)

        return label


    def deal_to_dealer(self):
        new_card = self.get_random_unplayed_card()
        new_card['in_play'] = True
        self._dealer_cards.append(new_card)

        self.hlayout_dealers_hand.insertWidget(self.hlayout_dealers_hand.count()-1, self.generate_card_widget(new_card))

        self._dealer_total = self.cards_total(self._dealer_cards)


    def deal_to_player(self):
        new_card = self.get_random_unplayed_card()
        new_card['in_play'] = True
        self._player_cards.append(new_card)

        self.hlayout_players_hand.insertWidget(self.hlayout_players_hand.count()-1, self.generate_card_widget(new_card))

        self._player_total= self.cards_total(self._player_cards)
        # print (self._player_total)


    def player_total(self):
        return self._player_total

    def dealer_total(self):
        return self._dealer_total

    def cards_total(self, cards : list):
        tot = 0
        for i in cards:
            tot += i['value']
        return tot


    # ==========================================================================
    # stats and progress
    def update_progress(self, n):
        self.progressBar.setProperty("value", n)


    def update_data_display(self):
        pass


    def update_n_games(self, n : int):
        self.lcd_n_games.setProperty("intValue", n)


    def get_step_games(self):
        return self.spinbox_n_games.value()






if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = blackjackBotUI()
    sys.exit(app.exec_())
