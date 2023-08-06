from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
import pandas as pd

from .activation import Activation
from .enum_regularization import Regularization


@dataclass
class Layer(metaclass=ABCMeta):
    input: pd.DataFrame = None
    output: pd.DataFrame = None
    activation: Activation = Activation.TANH
    regularization: Regularization = Regularization.NONE

    # computes the output Y of a layer for a given input X
    @abstractmethod
    def forward_propagation(self, input):
        return

    # computes dE/dX for a given dE/dY (and update parameters if any)
    @abstractmethod
    def backward_propagation(self, output_error, learning_rate):
        return
