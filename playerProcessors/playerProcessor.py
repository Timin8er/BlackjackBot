#!/usr/bin/env python
# import threading
# import multiprocessing
from playerBot import playerBot
from util.enums import playerState

# ==============================================================================
def player_process(n_bots, inbox_queue, outgoing_queue):
    # print (n_bots, inbox_queue, outgoing_queue)
    player_processor = playerProcessor(n_bots, inbox_queue, outgoing_queue)

    while True:
        message = inbox_queue.get()
        # print (message)

        if message[0] == 'begin_trials':
            player_processor.begin_trials(message[1])

        elif message[0] == 'start_game':
            player_processor.start_game()

        elif message[0] == 'initial_hithold':
            player_processor.hithold(message[1], True)

        elif message[0] == 'hithold':
            player_processor.hithold(message[1])

        elif message[0] == 'end_game':
            player_processor.end_game(message[1])

        elif message[0] == 'end_trials':
            player_processor.end_trials()

        elif message[0] == None:
            # Null message sent means end of life
            # print ('ending')
            break

    return player_processor.player_bots


# ==============================================================================
class playerProcessor(object):

    def __init__(self, n_bots, inbox_queue, outgoing_queue):
        self.player_bots = []
        self.n_bots = n_bots
        self.inbox_queue = inbox_queue
        self.outgoing_queue = outgoing_queue


    def begin_trials(self, player_bots):
        """
        breed the given bots to fill the n_bots quota
        """
        # print ('recieved %s bots' % len(player_bots))
        self.player_bots = player_bots

        index = 0
        while len(self.player_bots) < self.n_bots:
            self.player_bots.append(
                playerBot(self.player_bots[index])
            )
            index += 1
        # print ('generated %s bots' % index)


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
        print(total_in)


    def end_game(self, dealer_total : int, exposed_cards : list):
        """
        determine winners and loosers
        report player fitness
        """
        fitness_report = []
        for bot in self.player_bots:

            if bot.card_total > 21:
                bot.lose_game()
            elif self.game_ui.dealer_total() > 21:
                bot.win_game()
            elif bot.card_total < dealer_total:
                bot.lose_game()
            elif bot.card_total == dealer_total:
                bot.tie_game()
            elif bot.card_total > dealer_total:
                bot.win_game()

            fitness_report.append(bot.fitness())
        return fitness_report()



    def end_trials(self):
        """
        report the bots to the simulation controller for evolution
        """
        self.outgoing_queue.put(self.player_bots)