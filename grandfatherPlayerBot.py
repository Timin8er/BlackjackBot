from playerBot import playerBot
from nuralNetLayer import nuralNetLayer
import json

class grandfatherPlayerBot(playerBot):

    def __init__(self):
        playerBot.__init__(self)

        self.hh_nural_net = nuralNetLayer() # hti || hold Neural net
        self.eg_nural_net = nuralNetLayer() # end game neural net

        # get the pre defined nural net for the hit / hold decision
        with open('grandfatherHitHoldNuralNet.json') as nf:
            net = json.loads(nf.read())

            index = 0 # index of the data we loaded
            layer = self.hh_nural_net # current layer,
            while index < len(net): # iterate throught the loaded data
                if index != 0: # create a new layer if not on the first one
                    layer = layer.add_layer()

                # give the layer its weights and biases
                layer.weights = net[index]
                layer.biases = net[index+1]
                index += 2


        with open('grandfatherMemoryNuralNet.json') as nf:
            net = json.loads(nf.read())

            index = 0 # index of the data we loaded
            layer = self.eg_nural_net # current layer
            while index < len(net): # iterate throught the loaded data
                if index != 0: # create a new layer if not on the first one
                    layer = layer.add_layer()

                # give the layer its weights and biases
                layer.weights = net[index]
                layer.biases = net[index+1]
                layer.use_sigma = False
                index += 2

        # inp = [1]*24
        # self.eg_nural_net.feed_forward(inp)
