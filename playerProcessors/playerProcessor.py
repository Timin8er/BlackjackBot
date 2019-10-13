#!/usr/bin/env python
# import threading
# import multiprocessing
from playerBot import playerBot
from util.enums import playerState

# ==============================================================================
def player_process(n_bots, inbox_queue, outbox_queue):
    player_processor = playerProcessor(n_bots, inbox_queue, outbox_queue)

    while True:
        message = inbox_queue.get()

        if message[0] == 'begin_trials':
            player_processor.begin_trials(message[1])

        elif message[0] == 'start_game':
            player_processor.start_game()

        elif message[0] == 'hithold_ins':
            player_processor.hithold(message[1], True)

        elif message[0] == 'hithold':
            player_processor.hithold(message[1])

        elif message[0] == 'hithold':
            player_processor.insurence_payout(message[1])

        elif message[0] == 'end_game':
            player_processor.end_game(message[1], message[2])

        elif message[0] == 'end_trials':
            player_processor.end_trials()

        elif message[0] == None:
            # Null message sent means end of life
            break

    return player_processor.player_bots


# ==============================================================================
class playerProcessor(object):

    def __init__(self, n_bots, inbox_queue, outbox_queue):
        self.player_bots = []
        self.n_bots = n_bots
        self.inbox_queue = inbox_queue
        self.outbox_queue = outbox_queue


    def begin_trials(self, player_bots):
        """
        breed the given bots to fill the n_bots quota
        """
        self.player_bots = player_bots

        if len(self.player_bots) < 2:
            print ('%s: Too fiew bots, recieved %s' % (multiprocessing.current_process(), len(self.player_bots)))
        else:

            index = 0
            while len(self.player_bots) < self.n_bots:
                self.player_bots.append(
                    playerBot(self.player_bots[index])
                )
                index += 1


    def start_game(self):
        """
        reset all bots and ask for a bet
        """
        for bot in self.player_bots:
            bot.new_game_reset()
            bot.place_bet()


    def hithold(self, game_board_inputs : list, insurence_available = False):
        """
        ask for insurence bet, and first hithold
        """
        total_in = 0
        for bot in self.player_bots:
            inp = bot.hit_or_hold(game_board_inputs, insurence_available)
            if inp == playerState.In:
                total_in += 1
        # print(total_in)


    def insurence_payout(self, payout : bool):
        """
        process results of the insurance bets
        """
        if payout:
            for bot in self.player_bots:
                bot.money += bot.insurence
        else:
            for bot in self.player_bots:
                bot.money -= bot.insurence



    def end_game(self, dealer_total : int, exposed_cards : list):
        """
        determine winners and loosers
        report player fitness
        """
        fitness_report = []
        for bot in self.player_bots:

            if bot.card_total > 21:
                bot.lose_game()
            elif dealer_total > 21:
                bot.win_game()
            elif bot.card_total < dealer_total:
                bot.lose_game()
            elif bot.card_total == dealer_total:
                bot.tie_game()
            elif bot.card_total > dealer_total:
                bot.win_game()

            fitness_report.append(bot.fitness)
        self.outbox_queue.put(['fitness_update', fitness_report])



    def end_trials(self):
        """
        report the bots to the simulation controller for evolution
        """
        self.outbox_queue.put(['trials_complete',self.player_bots])
