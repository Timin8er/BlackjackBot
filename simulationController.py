#!/usr/bin/env python
from PyQt5.QtCore import QObject, pyqtSignal

from util.enums import simState, playerState
from dealerBot import dealerBot
from playerBot import playerBot
from playerHitHoldProcessor import playerHitHoldProcessor

import time

class simulationController(QObject):

    sim_state = simState.Paused

    def __init__(self, game_ui):
        QObject.__init__(self)
        self.game_ui = game_ui
        self.resume_at = self.state_new_game

        self.player_bots = []
        for i in range(100):
<<<<<<< refs/remotes/origin/development
            self.player_bots.append(playerBot(self.game_ui))
=======
            self.player_bots.append(self.generate_bot())
>>>>>>> Completed the loop

        self.dealer_bot = dealerBot(self, game_ui)

        self.player_hit_hold_processor = playerHitHoldProcessor(self.player_bots)
        self.player_hit_hold_processor.finished.connect(self.state_player_turn_end)
        self.player_hit_hold_processor.progress_update.connect(self.game_ui.update_progress)


    def set_sim_state(self, new_state):
        self.sim_state = new_state

        if new_state == simState.Paused:
            self.game_ui.action_pause()
        elif new_state == simState.Play:
            self.game_ui.action_play()
        elif new_state == simState.Step:
            self.game_ui.action_step()
        elif new_state == simState.StepGame:
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
        if self.sim_state == simState.Paused:
            self.set_sim_state(simState.Step)
        self.resume_at()


    def action_step_game(self):
        if self.sim_state == simState.Paused:
            self.set_sim_state(simState.StepGame)
        self.resume_at()


    # ==========================================================================
    # bot stuff

    def generate_bot(self):
        return playerBot(self.game_ui)

    # ==========================================================================
    # Simulation state machine

    def state_new_game(self):
        """
        Reset everything to the beginning of a game
        """
        print ('new game')
        self.game_ui.clear_board()
        self.game_ui.deal_to_dealer()
        self.game_ui.deal_to_player()
<<<<<<< refs/remotes/origin/development
        print ('starting with: %s' % self.game_ui.player_total())

        time.sleep(1)

        if self.sim_state == simState.Step:
=======

        if self.sim_state == simState.Step or self.sim_state == simState.Paused:
>>>>>>> Completed the loop
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
        print ('player turn: %s' % self.game_ui.player_total())

        self.player_hit_hold_processor.start()


    def state_player_turn_end(self):
        if self.player_hit_hold_processor.has_remaing_In and self.game_ui.player_total() < 22:
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

        # w/t/l
        for bot in self.player_bots:
            if bot.card_total > 21:
                bot.lose_game()
            elif bot.card_total < self.game_ui.dealer_total():
                bot.lose_game()
            elif bot.card_total == self.game_ui.dealer_total():
                bot.tie_game()
            elif bot.card_total > self.game_ui.dealer_total():
                bot.win_game()

        # delete broke bots
        for bot in reversed(self.player_bots):
            if bot.money <= 0:
                self.player_bots.remove(bot)

        # refill bots
        while len(self.player_bots) < 100:
            self.player_bots.append(self.generate_bot())

        self.game_ui.update_data_display()

        # if self.sim_state == simState.Play:
        #     self.state_new_game()
        # else:
        self.resume_at = self.state_new_game
        self.set_sim_state(simState.Paused)
