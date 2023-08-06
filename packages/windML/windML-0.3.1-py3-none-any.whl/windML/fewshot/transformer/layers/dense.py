from numpy import ndarray, broadcast_to
from numpy.random import randint 

from windML.fewshot.transformer.utils import ModelSettings

class DenseLayer:
    def __init__(self) -> None:
        pass 

    def forward(self, inputs: ndarray) -> ndarray:
        weights = randint(2, size=(inputs.shape[-1], ModelSettings.EMBEDDING_DIMENSION.value)) * ModelSettings.SCALING_FACTOR.value
        bias = randint(2, size=(ModelSettings.EMBEDDING_DIMENSION.value))
        outputs = inputs @ weights 
        outputs += broadcast_to(bias, outputs.shape)
        return outputs
    
    # def backward(self,inputs:ndarray,error:ndarray):
    #     dWeights = self._dWeights(inputs,error)            
    #     dInputs = self._dInputs(error)
    #     self.weights -= dWeights*ModelSettings.LEARNING_RATE.value
    #     dBias = None if self.bias is None else self._dBias(error)
    #     self.adam(dWeights, dBias)
    #     return dInputs
    
    # def adam(self, dWeights:ndarray, dBias:Optional[ndarray]) -> None:
    #     if self.vWeights is None:
    #         self.vWeights = dWeights
    #         self.sWeights = dWeights**2
            
    #     if dBias is not None:
    #         if self.vBias is None:
    #             self.vBias = dBias
    #             self.sBias = dBias**2
            
    #         self.vBias = self._vValue(self.vBias, dBias)
    #         self.sBias = self._sValue(self.sBias, dBias)
    #         self.bias -= self._dValue(self.vBias, self.sBias)
            
    #     self.vWeights = self._vValue(self.vWeights,dWeights)
    #     self.sWeights = self._sValue(self.sWeights, dWeights)
    #     self.weights -= self._dValue(self.vWeights, self.sWeights)

    # def _dInputs(self, error) -> ndarray:
    #     return error @ self.weights.transpose(0,-1,1)

    # @staticmethod
    # def _initialise_weights(n_heads:int,input_dimension:ndarray,output_dimension:ndarray) -> ndarray:
    #     weights = randn(n_heads,input_dimension,output_dimension) 
    #     weights *= sqrt(2/(n_heads*input_dimension))     
    #     return weights

    # @staticmethod
    # def _dWeights(inputs:ndarray, error:ndarray) -> ndarray:
    #     dWeights = inputs.transpose(0,1,-1,-2) @ error
    #     return dWeights.sum(axis=0)

    # @staticmethod
    # def _dBias(error:ndarray) -> ndarray:
    #     return error.sum(axis=0,keepdims=True).sum(axis=2,keepdims=True)

    # @staticmethod
    # def _vValue(vValue:ndarray, dValue:ndarray) -> ndarray:
    #     return vValue*ModelSettings.ADAM_ALPHA.value + dValue*(1-ModelSettings.ADAM_ALPHA.value)

    # @staticmethod
    # def _sValue(sValue:ndarray, dValue:ndarray) -> ndarray:
    #     return sValue*ModelSettings.ADAM_BETA.value + (dValue**2)*(1-ModelSettings.ADAM_BETA.value)

    # @staticmethod
    # def _dValue(vValue:ndarray, sValue:ndarray) -> ndarray:
    #     return vValue*ModelSettings.LEARNING_RATE.value / ( sqrt(sValue) + ModelSettings.ADAM_CONSTANT.value )
