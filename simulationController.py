#!/usr/bin/env python
from PyQt5.QtCore import QObject, pyqtSignal

from util.enums import simState, playerState
from dealerBot import dealerBot
from playerBot import playerBot
from grandfatherPlayerBot import grandfatherPlayerBot
from playerProcessors.processManager import processManager

import time
import numpy

class simulationController(QObject):

    sim_state = simState.Paused

    def __init__(self, game_ui, deck_controller):
        QObject.__init__(self)
        self.game_ui = game_ui
        self.deck_controller = deck_controller
        self.resume_at = self.run_trials
        self.n_bots = 400

        self.dealer_bot = dealerBot(self, game_ui)

        self.n_generations = 0
        self.step_n_games = 1
        self.n_games_generation = 0
        self.games_per_generation = 200

        # muliprocesses
        self.process_manager = processManager(self, self.n_bots)
        self.process_manager.start_processes()

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
    # bot stuff

    def generate_bot(self, parent_bot):
        return playerBot(self.game_ui, parent_bot)




    # ==========================================================================
    # Simulation state machine


    def run_trials(self):
        self.process_manager.begin_trials(self.player_bots)

        self.generate_game()



    def generate_game(self):
        self.deck_controller.clear_board()
        self.process_manager.start_game()

        self.deck_controller.deal_to_dealer()
        self.deck_controller.deal_to_player()
        self.deck_controller.deal_to_player()

        self.process_manager.initial_hithold(self.deck_controller.inputs()[0:11])









    def state_new_game(self):
        """
        Reset everything to the beginning of a game
        """
        self.player_bet_processor.start()

        # print ('new game')
        self.game_ui.clear_board()
        self.game_ui.deal_to_dealer()
        self.game_ui.deal_to_player()

        for bot in self.player_bots:
            bot.new_game_reset()

        if self.sim_state == simState.Step or self.sim_state == simState.Paused:
            self.set_sim_state(simState.Paused)
            self.resume_at = self.state_player_turn
        else:
            self.state_player_turn()


    def state_player_turn(self):
        """
        Iterate the players game once, determine the next step
        """
        # print ('player turn')
        self.game_ui.deal_to_player()
        self.player_hit_hold_processor.start()


    def state_player_turn_end(self):
        # print (self.game_ui.player_total(), self.player_hit_hold_processor.remaing_in)
        if self.player_hit_hold_processor.remaing_in and self.game_ui.player_total() < 22:
            if self.sim_state == simState.Step or self.sim_state == simState.Paused:
                self.resume_at = self.state_player_turn
                self.set_sim_state(simState.Paused)
            else:
                self.state_player_turn()
        else:
            if self.sim_state == simState.Step or self.sim_state == simState.Paused:
                self.resume_at = self.state_dealer_run
                self.set_sim_state(simState.Paused)
            else:
                self.state_dealer_run()


    def state_dealer_run(self):
        self.dealer_bot.run()

        if self.sim_state == simState.Step or self.sim_state == simState.Paused:
            self.resume_at = self.state_game_end
            self.set_sim_state(simState.Paused)
        else:
            self.state_game_end()


    def state_game_end(self):
        self.n_generations += 1
        self.n_games_generation += 1

        # win/tie/loss
        for bot in self.player_bots:

            if bot.card_total > 21:
                bot.lose_game()
            elif self.game_ui.dealer_total() > 21:
                bot.win_game()
            elif bot.card_total < self.game_ui.dealer_total():
                bot.lose_game()
            elif bot.card_total == self.game_ui.dealer_total():
                bot.tie_game()
            elif bot.card_total > self.game_ui.dealer_total():
                bot.win_game()


        # sort bots by fitness
        self.player_bots.sort(key=lambda x: x.fitness, reverse=True)

        # if it's time for a new generation
        if self.n_games_generation >= self.games_per_generation and self.player_bots[0].fitness != self.player_bots[50].fitness:
            self.n_games_generation = 0
            self.game_ui.update_generation_display(self.player_bots[0])

            # how many replacements?
            pops = int(len(self.player_bots)/2)
            # remove the worst
            for i in range(pops):
                # print ('pooping: %s' % self.player_bots.pop().fitness)
                self.player_bots.pop().fitness

            # replace
            i = 0
            while len(self.player_bots) < self.n_bots:
                # print ('breeding: %s' % self.player_bots[i].fitness)
                self.player_bots.append(self.generate_bot(self.player_bots[i]))
                # all bots tied for first, get a second offspring
                if self.player_bots[i].fitness == self.player_bots[0].fitness:
                    for i in range(3):
                        if len(self.player_bots) >= self.n_bots:
                            break
                        self.player_bots.append(self.generate_bot(self.player_bots[i]))
                i += 1

            # reset all bots
            for i in range(pops):
                self.player_bots[i].reset()

        self.game_ui.update_n_generations(self.n_generations)
        self.game_ui.update_data_display()


        # if we're stepping n games, tick down and process
        if self.sim_state == simState.StepGames:
            self.step_n_games -= 1
            if self.step_n_games == 0:
                self.resume_at = self.state_new_game
                self.set_sim_state(simState.Paused)
            else:
                self.state_new_game()
        # if normal play, continue
        elif self.sim_state == simState.Play:
            self.state_new_game()
        # else, we're pausing
        else:
            self.resume_at = self.state_new_game
            self.set_sim_state(simState.Paused)
