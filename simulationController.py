#!/usr/bin/env python
from PyQt5.QtCore import QObject, pyqtSignal

from util.enums import simState, playerState
from dealerBot import dealerBot
from playerBot import playerBot
from grandfatherPlayerBot import grandfatherPlayerBot
from playerHitHoldProcessor import playerHitHoldProcessor

import time
import numpy

class simulationController(QObject):

    sim_state = simState.Paused

    def __init__(self, game_ui):
        QObject.__init__(self)
        self.game_ui = game_ui
        self.resume_at = self.state_new_game
        self.n_bots = 100

        # generate grandfather bot
        self.grandfather_bot = grandfatherPlayerBot(self.game_ui)
        # print (self.grandfather_bot.nural_net.feedforward([16,99]))

        self.player_bots = []
        for i in range(self.n_bots):
            self.player_bots.append(playerBot(self.game_ui, self.grandfather_bot))

        self.dealer_bot = dealerBot(self, game_ui)

        self.player_hit_hold_processor = playerHitHoldProcessor(self.player_bots)
        self.player_hit_hold_processor.finished.connect(self.state_player_turn_end)
        self.player_hit_hold_processor.progress_update.connect(self.game_ui.update_progress)

        self.n_games = 0
        self.step_n_games = 1
        self.n_games_generation = 0


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

    def state_new_game(self):
        """
        Reset everything to the beginning of a game
        """
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
        # print ('player turn: %s' % self.game_ui.player_total())

        # print(self.game_ui.dealer_total(), self.game_ui.player_total())
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
        self.n_games += 1
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
        if self.n_games_generation > 250 and self.player_bots[0].fitness != self.player_bots[50].fitness:
            self.n_games_generation = 0

            # how many replacements?
            pops = int(len(self.player_bots)/2)
            # remove the worst
            for i in range(pops):
                self.player_bots.pop()

            # replace
            for i in range(pops):
                self.player_bots[i].reset()
                self.player_bots.append(self.generate_bot(self.player_bots[i]))


        self.game_ui.update_n_games(self.n_games)
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
