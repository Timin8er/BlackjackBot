#!/usr/bin/env python
from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer

from util.enums import simState, playerState
from dealerBot import dealerBot
from playerBot import playerBot
from grandfatherPlayerBot import grandfatherPlayerBot
from playerProcessors.processManager import processManager

import time
import numpy

class simulationController(QObject):

    sim_state = simState.Paused

    render_cards = pyqtSignal()

    def __init__(self, game_ui, deck_controller):
        QObject.__init__(self)
        self.game_ui = game_ui
        self.deck_controller = deck_controller
        self.resume_at = self.run_trials
        self.n_bots = 1000

        self.dealer_bot = dealerBot(self, deck_controller)

        self.n_generations = 0
        self.step_n_games = 1
        self.games_per_generation = 20
        self.n_games_generation = 0

        # muliprocesses
        self.process_manager = processManager(self, self.n_bots)
        self.process_manager.start_processes()

        self.process_manager.fitness_report.connect(self.game_ui.update_fitness_report)

        self.trials_thread = trialsThread(self)
        self.trials_thread.game_generated.connect(self.game_ui.render_game)

        # generate grandfather bot
        grandfather_bot = grandfatherPlayerBot()
        # print (self.grandfather_bot.nural_net.feed_forward([16,99]))

        self.player_bots = []
        for i in range(self.process_manager.n_processes * 2):
            self.player_bots.append(playerBot(grandfather_bot))


    def set_sim_state(self, new_state):
        self.sim_state = new_state

        if new_state == simState.Paused:
            self.game_ui.action_pause()
        elif new_state == simState.Play:
            self.game_ui.action_play()
        elif new_state == simState.Step:
            self.game_ui.action_step()
        elif new_state == simState.StepGames:
            self.game_ui.action_step_game()


    # ==========================================================================
    # user actions

    def action_pause(self):
        self.set_sim_state(simState.Paused)


    def action_play(self):
        if self.sim_state == simState.Paused:
            self.set_sim_state(simState.Play)
            self.resume_at()


    def action_step(self):
        t = self.sim_state
        self.set_sim_state(simState.Step)
        if t == simState.Paused:
            self.resume_at()


    def action_step_game(self):
        self.step_n_games = self.game_ui.get_step_games()
        t = self.sim_state
        self.set_sim_state(simState.StepGames)
        if t == simState.Paused:
            self.resume_at()


    # ==========================================================================
    # Simulation state machine
    def run_trials(self):
        # QTimer.singleShot(0,self.generate_trials)
        # self.generate_trials()
        self.trials_thread.start()


class trialsThread(QThread):

    game_generated = pyqtSignal(list,list,int)

    def __init__(self, sim_controller):
        QThread.__init__(self)

        self.s_c = sim_controller

    def __del__(self):
        self.wait()

    def run(self):
        # print('hi')
        self.generate_trials()


    def generate_trials(self):
        self.s_c.process_manager.begin_trials(self.s_c.player_bots)

        for i in range(self.s_c.games_per_generation):
            self.generate_game()
            # print('waiting')
            self.game_generated.emit(
                self.s_c.deck_controller.dealer_cards,
                self.s_c.deck_controller.player_cards,
                i+1)
            time.sleep(0.1)
            # print(self.s_c.deck_controller.dealer_cards)

        self.s_c.process_manager.end_trials()

        self.s_c.set_sim_state(simState.Paused)


    def generate_game(self):
        self.s_c.deck_controller.clear_board()
        self.s_c.process_manager.start_game()

        # initial hand
        self.s_c.deck_controller.deal_to_dealer()
        self.s_c.deck_controller.deal_to_player()
        self.s_c.deck_controller.deal_to_player()

        # if the dealer has an ace showing on the initial hand, ask for insurence
        if self.s_c.deck_controller.dealer_total == 11:
            self.s_c.process_manager.hithold_ins(self.s_c.deck_controller.inputs()[0:11])
        else:
            self.s_c.process_manager.hithold(self.s_c.deck_controller.inputs()[0:11])

        # continue dealing cards to the player untill we're over 21, bots leave
        # of their own choosing
        while self.s_c.deck_controller.player_total < 22:
            self.s_c.deck_controller.deal_to_player()
            self.s_c.process_manager.hithold(self.s_c.deck_controller.inputs()[0:11])

        # dealer reviels insurence
        if self.s_c.deck_controller.dealer_total == 11:
            self.s_c.deck_controller.deal_to_dealer()
            if self.s_c.deck_controller.dealer_total == 21:
                self.s_c.process_manager.insurence_payout(True)
            else:
                self.s_c.process_manager.insurence_payout(False)

        # dealer deals themselves cards
        while self.s_c.dealer_bot.hithold():
            self.s_c.deck_controller.deal_to_dealer()

        # determine winners
        self.s_c.process_manager.end_game(
            self.s_c.deck_controller.dealer_total,
            self.s_c.deck_controller.inputs()[0:10]
            )
