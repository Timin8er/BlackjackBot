#!/usr/bin/env python
import sys
import time
import json

from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow, QStyleFactory
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, QRect

import pyqtgraph

from simulationController import simulationController
from deckController import deckController
from blackjackBotMainWindow import Ui_MainWindow


class blackjackBotUI(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.show()

        self.card_widgets = []
        self.n_fitness_reports = 0

        self.deck_controller = deckController(self)
        self.sim_controller = simulationController(self, self.deck_controller)

        self.progressBar_deck.setMaximum(self.deck_controller.total_cards)
        self.progressBar_generated.setMaximum(self.sim_controller.games_per_generation)
        self.progressBar_simulated.setMaximum(self.sim_controller.games_per_generation)

        # timers
        self.last_fitness_report = None
        self.last_trials_report = None

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

        # add graphs
        self.fitness_history_best = []
        self.fitness_history_median = []

        self.current_fitness_plot = pyqtgraph.PlotWidget(title = 'Current Bot Money')
        self.verticalLayout.insertWidget(2, self.current_fitness_plot)
        self.fitness_history_plot = pyqtgraph.PlotWidget(title = 'Most Fit Bot, History')
        self.verticalLayout.insertWidget(3, self.fitness_history_plot)

        # set simulation labels
        self.printNBots.setText(str(self.sim_controller.n_bots))
        self.printNDecks.setText(str(self.deck_controller.n_decks))
        self.printNThreads.setText(str(self.sim_controller.process_manager.n_processes))
        self.printNGamesPerGen.setText(str(self.sim_controller.games_per_generation))

        self.bot_firness_baseline = 500




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

    def print_best_bot(self):
        file = 'archive/best_bot_' + str(time.time()) + '.json'
        with open(file, 'w+') as f:
            data = self.sim_controller.player_bots[0].to_dict()
            f.write(json.dumps(data))
            # f.write(str(self.sim_controller.player_bots[0].nural_net.weights))
            # f.write(str(self.sim_controller.player_bots[0].nural_net.biases))
            # f.write(str(self.sim_controller.player_bots[0].nural_net.next_layer.weights))
            # f.write(str(self.sim_controller.player_bots[0].nural_net.next_layer.biases))


    def clear_board(self):
        for c in self.card_widgets:
            c.deleteLater()
        self.card_widgets = []


    def render_game(self, dealer_cards, player_cards, game_number = 0, deck_progress = 0):
        self.clear_board()
        for c in dealer_cards:
            self.deal_to_dealer(c)
        for c in player_cards:
            self.deal_to_player(c)

        self.progressBar_generated.setProperty("value", game_number)
        self.progressBar_deck.setProperty("value", deck_progress)


    def generate_card_widget(self, card : dict):
        label = QLabel()
        pixmap = self._cards_sheet.copy(QRect(
            card['rank'] * self._cards_w,
            card['suit'] * self._cards_h,
            self._cards_w,
            self._cards_h))

        label.setPixmap(pixmap)
        self.card_widgets.append(label)
        return label


    def deal_to_dealer(self, card):
        self.hlayout_dealers_hand.insertWidget(self.hlayout_dealers_hand.count()-1, self.generate_card_widget(card))

    def deal_to_player(self, card):
        self.hlayout_players_hand.insertWidget(self.hlayout_players_hand.count()-1, self.generate_card_widget(card))


    # ==========================================================================
    # stats and progress

    def update_fitness_report(self, fitnesses: list):
        assert (isinstance(fitnesses, list)), 'invalid input type on fitnesses, expecting list, got %s' % type(fitnesses)
        new_time = time.time()
        if self.last_fitness_report is not None:
            dt = new_time - self.last_fitness_report
            self.printTGame.setText(str(round(dt,5)))
        self.last_fitness_report = new_time

        self.n_fitness_reports += 1
        self.current_fitness_plot.clear()
        self.current_fitness_plot.plot(fitnesses)
        self.progressBar_simulated.setProperty("value", self.n_fitness_reports)


    def update_end_trials(self, bots: list):
        new_time = time.time()
        if self.last_trials_report is not None:
            dt = new_time - self.last_trials_report
            self.printTGen.setText(str(round(dt,5)))
        self.last_trials_report = new_time

        self.n_fitness_reports = 0
        best_bot = bots[0]
        median_i = int(len(bots)/2)
        median_bot = bots[median_i]
        self.printBestAge.setText(str(best_bot.age))
        self.printBestDelta.setText(str(best_bot.fitness - median_bot.fitness))
        self.update_n_generations(self.sim_controller.n_generations)

        self.fitness_history_best.append(best_bot.fitness)
        self.fitness_history_median.append(median_bot.fitness)

        self.fitness_history_plot.clear()
        self.fitness_history_plot.plot(self.fitness_history_best, pen={'color': (0,0,255)})
        self.fitness_history_plot.plot(self.fitness_history_median, pen={'color': (173, 171, 14)})
        self.fitness_history_plot.plot([0,len(self.fitness_history_best)-1],[self.bot_firness_baseline,self.bot_firness_baseline], pen={'color': (71, 71, 71)})


    def update_n_generations(self, n : int):
        self.lcd_n_generations.setProperty("intValue", n)


    def get_step_games(self):
        return self.spinbox_n_games.value()


    def closeEvent(self, event):
        self.sim_controller.process_manager.__del__()
        event.accept()




if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = blackjackBotUI()
    sys.exit(app.exec_())
