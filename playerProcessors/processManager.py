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
        self.n_processes = multiprocessing.cpu_count()
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
        # print('processManager: recieved %s bots' % len(player_bots))

        split = math.ceil(len(player_bots) / self.n_processes)
        # print ('split : %s' % split)
        for i in range(self.n_processes):
            # print (i*self.bots_per,(i+1)*self.bots_per)
            # print (str(player_bots[0,1]))

            self.inbox_queues[i].put([
                'begin_trials',
                player_bots[i*split:(i+1)*split]
            ])



    def start_game(self):
        for i in self.inbox_queues:
            i.put(['start_game'])


    def initial_hithold(self, inputs):
        for i in self.inbox_queues:
            i.put(['initial_hithold', inputs])
