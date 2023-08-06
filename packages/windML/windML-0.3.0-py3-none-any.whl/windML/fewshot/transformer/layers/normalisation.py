from numpy import ndarray, sqrt, ones, zeros, mean

from windML.fewshot.transformer.utils import ModelSettings

class NormalisationLayer:
    def __init__(self) -> None:
        pass

    def forward(self, inputs: ndarray) -> ndarray:
        normalisation_dimensions = inputs.shape[1:] if len(inputs.shape) > 3 else inputs.shape
        averages = mean(inputs, keepdims=True)  
        variance = mean(inputs**2, keepdims=True) - averages ** 2
        normalised = (inputs - averages) / sqrt(variance + ModelSettings.AVOID_DIVISION_BY_ZERO.value) 
        gain = ones(shape=normalisation_dimensions) 
        bias = zeros(shape=normalisation_dimensions) 
        return gain * normalised + bias

    # def backward(self,error:ndarray) -> ndarray:
    #     batch_size = self.normalised.shape[-1]
    #     normalised_inputs = self.inputs-mean(self.inputs,axis=-1,keepdims=True)
    #     normalised_error = normalised_inputs*error
    #     total_normalised_error = normalised_error.sum(axis=-1,keepdims=True)
    #     total_error = error.sum(axis=-1,keepdims=True)
    #     batch_error = batch_size*error-total_error
    #     a = sqrt(self.variance)*batch_error-self.norm*total_normalised_error
    #     b = batch_size*self.variance
    #     return a / b

    # @staticmethod
    # def _normalise(inputs:ndarray, variance:ndarray) -> ndarray:
    #     return ( inputs - mean(inputs,axis=-1,keepdims=True) ) / sqrt(variance)
