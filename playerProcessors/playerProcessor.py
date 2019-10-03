#!/usr/bin/env python
from PyQt5.QtCore import QThread
import threading
import multiprocessing

class playerProcessor(QThread):

    def __init__(self, sim_controller, player_bots : list):
        QThread.__init__(self)
        self.player_bots = player_bots
        self.sim_controller = sim_controller
        self.n_threads = self.sim_controller.n_threads

    # Qthread run function,
    def run(self):
        threads = []
        for i in range(self.n_threads):
            t = threading.Thread(target=self.thread_run, args=(i,))
            threads.append(t)

        for i in threads:
            i.start()

        for i in threads:
            i.join()

        threads = []


    # iterate through bots
    def thread_run(self, index):
        while index < len(self.player_bots):
            self.operation(self.player_bots[index])
            index += self.n_threads

    # operate on the bot
    def operation(self, bot):
        pass
