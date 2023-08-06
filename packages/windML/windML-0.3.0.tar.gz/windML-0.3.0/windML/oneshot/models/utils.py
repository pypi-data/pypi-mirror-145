from enum import Enum 

from numpy import ndarray, exp, sqrt

class ModelSettings(Enum):
    HIDDEN_DIMENSION = 100
    WEIGHT_FACTOR = 1e-5
    RESET_THRESHOLD = 1e-3
    NORMALISATION_FACTOR = 1e-6

def sigmoid(inputs:ndarray) -> ndarray:
    return 1 / ( 1 + exp(-inputs))

def normalisation_layer(inputs:ndarray) -> ndarray:
    inputs_variance = inputs-inputs.mean()
    inputs_variance_positive = sqrt(inputs.var() + ModelSettings.NORMALISATION_FACTOR.value)
    return inputs_variance/inputs_variance_positive