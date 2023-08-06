from numpy import ndarray, arange, newaxis, cos, sin, power

from windML.fewshot.transformer.utils import ModelSettings


class PositionEncodingLayer:
    def __init__(self) -> None:
        pass

    def forward(self, inputs: ndarray) -> ndarray:
        sequence_length = inputs.shape[0]
        position_encodings = self._position_encodings(
            positions=arange(sequence_length)[:, newaxis],
            indexes=arange(ModelSettings.EMBEDDING_DIMENSION.value)[newaxis, :]
        )
        if len(inputs.shape) <= 1: 
            position_encodings = position_encodings[newaxis,...]
        return inputs + position_encodings
        
    def backward(self) -> None:
        pass

    @staticmethod
    def _position_encodings(positions:ndarray, indexes:ndarray):
        angles = 1 / power(10000., (2*(indexes//2)) / ModelSettings.EMBEDDING_DIMENSION.value)
        angles = positions * angles
        angles[:, 0::2] = sin(angles[:, 0::2])
        angles[:, 1::2] = cos(angles[:, 1::2])
        return angles