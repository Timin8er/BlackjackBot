from playerBot import playerBot
from nuralNetLayer import nuralNetLayer
# import numpy

class grandfatherPlayerBot(playerBot):

    def __init__(self, board_controller):
        playerBot.__init__(self, board_controller)

        self.nural_net = nuralNetLayer()
        self.nural_net.weights = [[-2,0,0,0],[-3,0,0,0],[-4,0,0,0],[-5,0,0,0],[-6,0,0,0],[-7,0,0,0],[-8,0,0,0],[-9,0,0,0],[-10,0,0,0],[-11,0,0,0],[0,0,0,0]]
        self.nural_net.biases = [16,0,0,0]

        # inp = [1,0,0,0,2,0,0,0,0,0,0]
        # print (numpy.dot(inp, self.nural_net.weights))
        # print (self.feed_forward(inp))

        layer2 = self.nural_net.add_layer()
        layer2.weights = [[1],[0],[0],[0]]
        layer2.biases = [-0.5]


        # print (self.feed_forward(inp))
