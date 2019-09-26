from playerBot import playerBot
from nuralNetLayer import nuralNetLayer

class grandfatherPlayerBot(playerBot):

    def __init__(self, board_controller):
        playerBot.__init__(self, board_controller)

        self.nural_net = nuralNetLayer()
        self.nural_net.weights = [[-1],[0]]
        self.nural_net.biases = [16]
