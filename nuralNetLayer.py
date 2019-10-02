import numpy
import copy

class nuralNetLayer(object):

    def __init__(self, previouse_layer=None, parent=None):

        self.previouse_layer = None
        self.next_layer = None

        if previouse_layer:
            self.previouse_layer = previouse_layer
            self.previouse_layer.next_layer = self

        if parent:
            self.weights = copy.deepcopy(parent.weights)
            self.weights = self.random_adjust(self.weights)

            self.biases = copy.deepcopy(parent.biases)
            self.biases = self.random_adjust(self.biases)

            if parent.next_layer:
                self.add_layer(parent.next_layer)

        # print ('weights: %s' % self.weights)
        # print ('biases: %s' % self.biases)

    def feed_forward(self, inputs):
        # calculate self
        outputs = numpy.add(numpy.dot(inputs, self.weights), self.biases)

        outputs = self.sigma(outputs)

        # propagate forward
        if self.next_layer:
            return self.next_layer.feed_forward(outputs)
        return outputs


    def add_layer(self, parent=None):
        if self.next_layer:
            self.next_layer.add_layer(parent)
        else:
            self.next_layer = nuralNetLayer(previouse_layer=self, parent=parent)
        return self.next_layer


    def sigma(self, x):
        return 1 / (1 + numpy.exp(-x))


    def random_adjust(self, input):
        if isinstance(input, list):
            for i in range(len(input)):
                input[i] = self.random_adjust(input[i])
            return input
        else:
            input *= numpy.random.normal(1, 0.1)
            input += numpy.random.normal(0, 0.05)
            return input
