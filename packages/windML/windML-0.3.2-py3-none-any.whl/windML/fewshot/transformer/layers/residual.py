from numpy import ndarray, ones, broadcast_to, maximum 
from numpy.random import randint

class ResidualLayer:
    def __init__(self) -> None:
        pass

    def forward(self, inputs: ndarray, output_dimension:int) -> ndarray:
        weights_residual = randint(5, size=(inputs.shape[-1], output_dimension))
        bias_residual = ones(shape=(output_dimension))
        outputs = inputs @ weights_residual
        outputs += inputs 
        outputs += broadcast_to(bias_residual, outputs.shape)
        return self.relu(outputs) 

    def backward(self) -> None:
        pass

    @staticmethod
    def relu(inputs: ndarray) -> ndarray:
        return maximum(inputs, 0, inputs)