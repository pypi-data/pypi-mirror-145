from numpy import ndarray
from numpy.random import rand

from windML.fewshot.transformer.utils import ModelSettings

class DropoutLayer:
    def __init__(self) -> None:
        pass

    def dropout_layer(self, inputs: ndarray) -> ndarray:
        probability = 1. - ModelSettings.DROPOUT_RATE.value
        keep = rand(*inputs.shape) < probability
        outputs = inputs * keep
        outputs /= probability
        return outputs

    def backward(self) -> None:
        pass
