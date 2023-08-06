from enum import Enum
import numpy as np


class Activation(Enum):
    RELU = 0
    TANH = 1
    SIGMOID = 2
    LINEAR = 3
    SOFTMAX = 4

    @classmethod
    def sigmoid(self, z):
        return 1 / (1 + np.e ** -z)

    @classmethod
    def d_sigmoid(self, z):
        return np.divide(np.exp(-z), np.power(1 + np.exp(-z), 2))

    @classmethod
    def tanh(self, z):
        return np.tanh(z)

    @classmethod
    def d_tanh(self, z):
        return 1 - (np.tanh(z) ** 2)

    @classmethod
    def relu(self, z):
        return z * (z > 0)

    @classmethod
    def d_relu(self, z):
        return 1. * (z >= 0)
    
    @classmethod
    def softmax(self, z):
        """applies softmax to an input x"""
        e_x = np.exp(z)
        return e_x / e_x.sum()
    
    def sigmoid_derivative(self, Z):
        s = 1 / (1 + np.exp(-Z))
        return s * (1 - s)
    
    @classmethod
    def d_softmax(self, X, Y, store):
        derivatives = {}
 
        store["A0"] = X.T
 
        A = store["A" + str(self.L)]
        dZ = A - Y.T
 
        dW = dZ.dot(store["A" + str(self.L - 1)].T) / self.n
        db = np.sum(dZ, axis=1, keepdims=True) / self.n
        dAPrev = store["W" + str(self.L)].T.dot(dZ)
 
        derivatives["dW" + str(self.L)] = dW
        derivatives["db" + str(self.L)] = db
 
        for l in range(self.L - 1, 0, -1):
            dZ = dAPrev * self.sigmoid_derivative(store["Z" + str(l)])
            dW = 1. / self.n * dZ.dot(store["A" + str(l - 1)].T)
            db = 1. / self.n * np.sum(dZ, axis=1, keepdims=True)
            if l > 1:
                dAPrev = store["W" + str(l)].T.dot(dZ)
 
            derivatives["dW" + str(l)] = dW
            derivatives["db" + str(l)] = db
 
        return derivatives


def activate(activation, z):
    match activation:
        case Activation.RELU:
            return activation.relu(z)
        case Activation.TANH:
            return activation.tanh(z)
        case Activation.SIGMOID:
            return activation.sigmoid(z)
        case Activation.SOFTMAX:
            return activation.softmax(z)
        case Activation.LINEAR:
            return z



def d_activate(activation, z):
    match activation:
        case Activation.RELU:
            return activation.d_relu(z)
        case Activation.TANH:
            return activation.d_tanh(z)
        case Activation.SIGMOID:
            return activation.d_sigmoid(z)
        case Activation.SOFTMAX:
            return activation.d_softmax(z)
        case Activation.LINEAR:
            return z
