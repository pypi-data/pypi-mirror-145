from enum import Enum
import numpy as np


class Loss(Enum):
    MSE = 0
    CROSS_ENTROPY = 1

    @classmethod
    def mse(self, y_true, y_pred):
        return np.square(np.subtract(y_true,y_pred)).mean()

    @classmethod
    def d_mse(self, y_true, y_pred):
        return 2 * (y_pred - y_true) / y_true.size

    @classmethod
    def cross_entropy(self, h, y):
        h = np.clip(h, 0.000000001, 0.99999999)
        return np.mean(-y * np.log(h) - (1 - y) * np.log(1 - h))

    


def calculate_loss(loss, y_true, y_pred):
    match loss:
        case Loss.MSE:
            return loss.mse(y_true, y_pred)
        case Loss.CROSS_ENTROPY:
            return loss.cross_entropy(y_true, y_pred)


def calculate_d_loss(loss, y_true, y_pred):
    match loss:
        case Loss.MSE:
            return loss.d_mse(y_true, y_pred)
        case Loss.CROSS_ENTROPY:
            return loss.d_mse(y_true, y_pred)
