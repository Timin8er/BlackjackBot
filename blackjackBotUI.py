#!/usr/bin/env python
import sys
import random
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow, QStyleFactory
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, QRect

import pyqtgraph
import numpy

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

        self.sim_controller = simulationController(self)
        self.total_bots = self.sim_controller.player_bots
        self.progressBar_simulated.setMaximum(self.sim_controller.games_per_generation)
        self.progressBar_generated.setMaximum(self.sim_controller.games_per_generation)

        # menu actions
        self.actionPrintBestBot.triggered.connect(self.print_best_bot)

        # controll button icons
        self.btn_pause.setIcon(QIcon('icons/pause.png'))
        self.btn_step.setIcon(QIcon('icons/skip-forward.png'))
        self.btn_step_round.setIcon(QIcon('icons/double-skip-forward.png'))
        self.btn_play.setIcon(QIcon('icons/play.png'))

        # controll button functions
        self.btn_pause.clicked.connect(self.action_pause)
        self.btn_pause.clicked.connect(self.sim_controller.action_pause)
        self.btn_play.clicked.connect(self.action_play)
        self.btn_play.clicked.connect(self.sim_controller.action_play)
        self.btn_step_round.clicked.connect(self.action_step_game)
        self.btn_step_round.clicked.connect(self.sim_controller.action_step_game)
        self.btn_step.clicked.connect(self.action_step)
        self.btn_step.clicked.connect(self.sim_controller.action_step)

        self.btn_pause.setEnabled(False)

        QApplication.setStyle(QStyleFactory.create('Fusion'))

        with open('style.css') as s:
            self.setStyleSheet(s.read())

        self._cards_sheet = QPixmap('icons/cards.png')
        self._cards_w = self._cards_sheet.width() / 13
        self._cards_h = self._cards_sheet.height() / 4

        self._dealer_cards = []
        self._player_cards = []
        self._player_cards_input = [0,0,0,0,0,0,0,0,0,0]

        self._dealer_total = 0
        self._player_total = 0

        # add graphs
        self.fitness_history = []
        self.fitness_history_recent = []

        self.current_fitness_plot = pyqtgraph.PlotWidget(title = 'Current Bot Money')
        self.verticalLayout.insertWidget(2, self.current_fitness_plot)
        self.fitness_history_plot = pyqtgraph.PlotWidget(title = 'Most Fit Bot, History')
        self.verticalLayout.insertWidget(3, self.fitness_history_plot)



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
        self.progressBar_bots.setProperty("value", 0)

        for i in self._dealer_cards:
            i['object'].deleteLater()
        for i in self._player_cards:
            i['object'].deleteLater()

        self._dealer_cards = []
        self._player_cards = []
        self._player_cards_input = [0,0,0,0,0,0,0,0,0,0]
        self._dealer_total = 0
        self._player_total = 0

        for i in self.deck:
            i['in_play'] = False


    def print_best_bot(self):
        with open('best_bot', 'w') as f:
            f.write(str(self.sim_controller.player_bots[0].nural_net.weights))
            f.write(str(self.sim_controller.player_bots[0].nural_net.biases))
            f.write(str(self.sim_controller.player_bots[0].nural_net.next_layer.weights))
            f.write(str(self.sim_controller.player_bots[0].nural_net.next_layer.biases))


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
        self._player_cards_input[new_card['value'] - 2] += 1

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
        self.progressBar_bots.setProperty("value", n)


    def update_data_display(self):
        fit = []
        for bot in self.sim_controller.player_bots:
            fit.append(bot.fitness)

        self.current_fitness_plot.clear()
        self.current_fitness_plot.plot(fit, symbol='o', pen=None)

        self.progressBar_generation.setProperty("value", (self.sim_controller.n_games_generation))


    def update_generation_display(self, most_fit_bot):
        self.fitness_history.append(most_fit_bot.fitness)
        self.fitness_history_recent.append(most_fit_bot.fitness)
        # if len(self.fitness_history_recent) > 100:
        #     self.fitness_history_recent.pop(0)
        self.fitness_history_plot.clear()
        self.fitness_history_plot.plot(self.fitness_history_recent)

        n = 0
        for bot in self.sim_controller.player_bots:
            if bot.original:
                n+=1
        self.printNOriginals.setText(str(n))


    def update_n_games(self, n : int):
        self.lcd_n_games.setProperty("intValue", n)


    def get_step_games(self):
        return self.spinbox_n_games.value()


    def closeEvent(self, event):
        self.sim_controller.process_manager.end_processes()
        event.accept()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = blackjackBotUI()
    sys.exit(app.exec_())
