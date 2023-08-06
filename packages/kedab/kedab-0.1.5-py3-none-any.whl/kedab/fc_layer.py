from dataclasses import dataclass
from layer import Layer
import numpy as np

# inherit from base class Layer

class FCLayer(Layer):
    def __init__(self, input_size, output_size):
        # y = 1.0/np.sqrt(input_size)
        # self.weights = np.full(shape=(input_size,output_size), fill_value=0.001)
        # self.bias = np.full(shape=(1,output_size), fill_value=0.001)
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5

    # returns output for a given input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output

    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward_propagation(self, output_error, learning_rate):
        input_error = np.dot(output_error, self.weights.T)
        # if not isinstance(self.input, np.ndarray):
        #    self.input = self.input.ravel()

        weights_error = np.dot(self.input.T, output_error)
        # dBias = output_error

        # update parameters
        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * output_error
        return input_error
