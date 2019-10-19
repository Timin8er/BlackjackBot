#!/usr/bin/env python3
from PyQt5.QtCore import QObject, pyqtSignal
import threading
import multiprocessing
import math

from playerProcessors import playerProcessor

class processManager(QObject):

    fitness_report = pyqtSignal(list)
    trials_complete = pyqtSignal(list)

    def __init__(self, sim_controller, start_n_bot):
        QObject.__init__(self)
        self.sim_controller = sim_controller
        self.n_processes = multiprocessing.cpu_count() - 1
        self.bots_per = int(start_n_bot / self.n_processes)
        self.sim_controller.n_bots = self.bots_per * self.n_processes

        # print ('Processes: %s' % self.n_processes)
        # print ('Bots Per: %s' % self.bots_per)
        # print ('Total Bots: %s' % self.sim_controller.n_bots)

        self.processes = [] # the processes doint the processing
        self.inbox_queues = [] # the process inboxes
        self.outbox_queues = [] # the process outboxes


        # there is an inbound and outbound queue for each bot processor
        for i in range(self.n_processes):
            self.inbox_queues.append(
                multiprocessing.Queue()
            )
            self.outbox_queues.append(
                multiprocessing.Queue()
            )

        self.process_listener = processListener(self, self.outbox_queues)
        self.process_listener.start()

    def __del__(self):
        self.outbox_queues[0].put('end')
        self.end_processes()


    def start_processes(self):
        if self.processes:
            self.end_processes()

        for i in range(self.n_processes):
            p = multiprocessing.Process(target=playerProcessor.player_process, args=(
            #     self.player_bots[i*bots_per:(i+1)*bots_per],
                self.bots_per,
                self.inbox_queues[i],
                self.outbox_queues[i]))
            self.processes.append(p)
            p.start()


    # end the processes
    def end_processes(self):
        for q in self.inbox_queues:
            q.put([None])

        for p in self.processes:
            p.join()
        self.processes = []


    def begin_trials(self, player_bots:list):
        # by rounding up we ensure that the splis is slightly greater, when the
        # bots don't devide evenly
        split = math.ceil(len(player_bots) / self.n_processes)
        # print ('split : %s' % split)
        for i in range(self.n_processes):
            self.inbox_queues[i].put([
                'begin_trials',
                # if the bots did not devide evenly, the last queue will be short
                player_bots[i*split:(i+1)*split]
            ])



    def start_game(self):
        for i in self.inbox_queues:
            i.put(['start_game'])


    def hithold_ins(self, inputs):
        for i in self.inbox_queues:
            i.put(['hithold_ins', inputs])

    def hithold(self, inputs):
        for i in self.inbox_queues:
            i.put(['hithold', inputs])

    def insurence_payout(self, payout : bool):
        for i in self.inbox_queues:
            i.put(['insurence_payout', payout])

    def end_game(self, dealer_total, exposed_cards, shuffle):
        for i in self.inbox_queues:
            i.put(['end_game', dealer_total, exposed_cards, shuffle])

    def end_trials(self):
        for i in self.inbox_queues:
            i.put(['end_trials'])



class processListener(threading.Thread):
    """
    This thread listens to the processer outboxes and activates signals when messages come through
    """
    def __init__(self, process_manager, outboxes):
        threading.Thread.__init__(self)
        self.process_manager = process_manager
        self.outboxes = outboxes


    def run(self):
        while True:
            outs = []
            for o in self.outboxes:
                outs.append(o.get())
                if outs[-1] == 'end':
                    break

            if outs[-1] == 'end':
                break

            if outs[0][0] == 'fitness_update':
                fits = []
                for i in outs:
                    fits.extend(i[1])
                fits.sort(reverse=True)
                self.process_manager.fitness_report.emit(fits)

            elif outs[0][0] == 'trials_complete':
                # print('trials complete')
                bots = []
                for i in outs:
                    bots.extend(i[1])
                bots.sort(key=lambda x: x.fitness, reverse=True)

                self.process_manager.trials_complete.emit(bots)
