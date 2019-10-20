from playerBot import playerBot
from nuralNetLayer import nuralNetLayer
import json
import sys
import os

class grandfatherPlayerBot(playerBot):

    def __init__(self):
        playerBot.__init__(self)

        self.hh_nural_net = nuralNetLayer() # hti || hold Neural net
        self.eg_nural_net = nuralNetLayer() # end game neural net

        # get the pre defined nural net for the hit / hold decision
        if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
            file = sys.argv[1]
        else:
            file = 'archive/grandfather.json'

        with open(file) as nf:
            net = json.loads(nf.read())

            self.build_from_dict(net)

        # inp = [1]*24
        # self.eg_nural_net.feed_forward(inp)
