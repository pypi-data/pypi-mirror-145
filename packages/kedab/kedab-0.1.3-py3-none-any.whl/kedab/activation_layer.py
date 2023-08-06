from dataclasses import dataclass
from layer import Layer
from activation import Activation, activate, d_activate


@dataclass
class ActivationLayer(Layer):
    activation: Activation

    # returns the activated input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = activate(self.activation, self.input)
        return self.output

    # Returns input_error=dE/dX for a given output_error=dE/dY.
    # learning_rate is not used because there is no "learnable" parameters.
    def backward_propagation(self, output_error, learning_rate):
        return d_activate(self.activation, self.input) * output_error
