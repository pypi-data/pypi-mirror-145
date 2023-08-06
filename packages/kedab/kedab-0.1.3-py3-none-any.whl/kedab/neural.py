from activation import Activation
from enum_regularization import Regularization
from enum_optimizer import Optimizer
from loss import Loss, calculate_d_loss, calculate_loss
from layer import Layer

from typing import List
import numpy as np
from dataclasses import dataclass
import pandas as pd
from dotmap import DotMap
from json import load
import matplotlib.pyplot as plt


@dataclass
class NeuralNetwork:
    # layers: List[Layer] = field(init)
    # add layer to network
    def __init__(self):
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)

    def compile(self, learning_rate: float, loss: Loss, optimizer: Optimizer):
        self.learning_rate = learning_rate
        self.loss = loss
        self.optimizer = optimizer

    # predict output for given input
    def predict(self, input_data) -> np.ndarray:
        output = input_data
        # forward propagation
        # outputs = []
        for layer in self.layers:
            output = layer.forward_propagation(output)
        return np.array(output)

    def fit(self, x_train, y_train, epochs):
        # x_train = x_train.to_numpy()
        # sample dimension first
        self.error_list = []
        epochs_list = []
        samples = len(x_train)

        # training loop
        for i in range(epochs):
            error_sum = 0
            for j in range(samples):
                # forward propagation
                output = np.array(x_train[j], ndmin=2)
                for layer in self.layers:
                    output = layer.forward_propagation(output)

                # compute loss (for display purpose only)
                error_sum += calculate_loss(self.loss, y_train[j], output)

                # backward propagation
                error = calculate_d_loss(self.loss, y_train[j], output)
                for layer in reversed(self.layers):
                    error = layer.backward_propagation(error, self.learning_rate)

            # calculate average error on all samples
            error_sum /= samples
            self.error_list.append(error_sum)
            epochs_list.append(i)
            print(f"Epoch: {i+1}/{epochs}   error={error_sum}")
        # loss_graph(self.error_list, epochs_list)

        # return error_list

    # TODO What is going on here?
    def d_loss_function(self, true_labels, probabilities):
        probabilities = self.sigmoid(probabilities)
        return -np.divide(true_labels, probabilities) + np.divide(
            1 - true_labels, 1 - probabilities
        )


def loss_graph(error_list, epochs_list):
    plt.plot(epochs_list, error_list, "g", label="Error loss")
    plt.title("Training loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()


# TODO Make sure that the layers and their structures can be added and parsed directly via JSON, too
def create_network_from_hyperparameters(
    x: pd.DataFrame, y: pd.DataFrame, layers: List[Layer], param_path: str
) -> NeuralNetwork:
    with open(param_path) as f:
        params = DotMap(load(f))
        neural_network = NeuralNetwork(
            x,
            y,
            layers,
            params.epoch,
            params.learning_rate,
            params.bias,
            Activation[params.activation],
            Regularization[params.regularization],
            Loss[params.loss],
        )
        print(neural_network.__dict__)
        return neural_network
