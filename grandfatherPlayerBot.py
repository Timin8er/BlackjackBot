from playerBot import playerBot
from nuralNetLayer import nuralNetLayer
import json

class grandfatherPlayerBot(playerBot):

    def __init__(self):
        playerBot.__init__(self)

        self.nural_net = nuralNetLayer()

        # get the pre defined nural net
        with open('grandfatherPlayerNuralNet.json') as nf:
            net = json.loads(nf.read())

            index = 0 # index of the data we loaded
            layer = self.nural_net # current layer
            while index < len(net): # iterate throught the loaded data
                if index != 0: # create a new layer if not on the first one
                    layer = layer.add_layer()

                # give the layer its weights and biases
                layer.weights = net[index]
                layer.biases = net[index+1]
                index += 2
