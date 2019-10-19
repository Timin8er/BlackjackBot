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
        self.n_bots = 400

        self.dealer_bot = dealerBot(self, deck_controller)

        self.n_generations = 0
        self.step_n_games = 1
        self.games_per_generation = 150

        # muliprocesses
        self.process_manager = processManager(self, self.n_bots)
        self.process_manager.start_processes()

        self.process_manager.fitness_report.connect(self.game_ui.update_fitness_report)
        self.process_manager.trials_complete.connect(self.game_ui.update_end_trials)
        self.process_manager.trials_complete.connect(self.end_trials)

        self.trials_thread = trialsThread(self)
        self.trials_thread.game_generated.connect(self.game_ui.render_game)

        # generate grandfather bot
        grandfather_bot = grandfatherPlayerBot()
        # print (self.grandfather_bot.nural_net.feed_forward([16,99]))

        self.player_bots = []
        for i in range(self.process_manager.n_processes *2):
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
        self.n_generations += 1
        self.trials_thread.start()


    def end_trials(self, bots):
        self.player_bots = bots.copy()
        median_i = int(len(bots)/2)
        median_fitness = bots[median_i].fitness
        best_fitness = bots[0].fitness

        # if the best and median scores are to close, don't breed
        # if self.player_bots[0].fitness - median_fitness < 10:
        #     print ('Skipping Breeding, delta 0 - median < 5')
        if self.player_bots[self.process_manager.n_processes*2].fitness == median_fitness:
            print ('Skipping Breeding, fitness[2xCpuCount] = fitness[median] = %s' % median_fitness)
            for bot in self.player_bots:
                bot.reset()
        else:
            # remove worst ~half of bots
            d_count = 0
            for bot in reversed(self.player_bots):
                if bot.fitness <= median_fitness:
                    self.player_bots.remove(bot)
                    d_count+=1
                else:
                    bot.reset()

            # git the best bot a breading edge
            for i in range(5):
                self.player_bots.append(playerBot(self.player_bots[0]))
                self.player_bots.append(playerBot(self.player_bots[1]))
                self.player_bots.append(playerBot(self.player_bots[2]))

        print ('Round %s: %s bots deleted, best fitness = %s, median fitness = %s' % (self.n_generations, d_count, best_fitness, median_fitness))

        if self.sim_state == simState.Play:
            self.run_trials()
        elif self.sim_state == simState.StepGames:
            self.step_n_games -= 1
            if self.step_n_games == 0:
                self.set_sim_state(simState.Paused)
            else:
                self.run_trials()
        else:
            self.set_sim_state(simState.Paused)



class trialsThread(QThread):

    game_generated = pyqtSignal(list,list,int,int)

    def __init__(self, sim_controller):
        QThread.__init__(self)

        self.s_c = sim_controller
        self.signal_frequency = 5
        self.signal_frequency_i = 0

    def __del__(self):
        self.wait()

    def run(self):
        """
        Generate a set of trials consisting of n number of games
        """
        self.s_c.process_manager.begin_trials(self.s_c.player_bots)

        for i in range(self.s_c.games_per_generation):
            self.generate_game()
            # print('waiting')
            self.signal_frequency_i += 1
            if self.signal_frequency_i == self.signal_frequency:
                self.signal_frequency_i = 0
                self.game_generated.emit(
                    self.s_c.deck_controller.dealer_cards,
                    self.s_c.deck_controller.player_cards,
                    i+1,
                    self.s_c.deck_controller.deck_progress)
            time.sleep(0.02)
            # print(self.s_c.deck_controller.dealer_cards)

        self.s_c.process_manager.end_trials()

        # self.s_c.set_sim_state(simState.Paused)


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
            self.s_c.deck_controller.inputs()[11:21],
            0
            )
