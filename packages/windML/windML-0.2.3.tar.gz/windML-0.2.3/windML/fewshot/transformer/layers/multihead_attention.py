from typing import Dict

from numpy import array, exp, ndarray, sqrt
from numpy.random import randint

class MultiHeadAttention:
    def __init__(self) -> None:
        pass

    def forward(self, Q:Dict[int,callable], K: Dict[int,callable], V: Dict[int,callable]) -> ndarray:
        attention_matrix = list()
        for index in Q.keys():
            logits = Q[index] @ K[index].T / sqrt(K[index].shape[1]) 
            outputs = self.softmax(logits)  
            attention_matrix.append(outputs @ V[index])

        attention_matrix = array(attention_matrix) 
        attention_heads = attention_matrix.reshape(self._permute_shape(attention_matrix)) 
        attention = attention_heads.reshape(attention_heads.shape[0], -1)  

        weights = randint(3, size=(attention.shape[-1], attention_matrix.shape[-1])) 
        return attention @ weights   

    def backward(self) -> None:
        pass

    @staticmethod
    def softmax(inputs: ndarray) -> ndarray:
        e = exp(inputs - max(inputs))
        return e / e.sum(axis=-1)

    @staticmethod
    def _permute_shape(inputs: ndarray) -> tuple:
        if len(inputs.shape) > 3:
            batch, heads, sequence_length, embeddings_size = inputs.shape
            return batch, sequence_length, heads, embeddings_size
        heads, sequence_length, embedding_size = inputs.shape
        return sequence_length, heads, embedding_size

    
    # def softmax_backward(self,error:ndarray) -> ndarray:
    #     return self.output * (error - sum( self.output * error, axis=-1, keepdims=True) )

    # def backward(self,inputs:ndarray, error:ndarray) -> Tuple[ndarray,ndarray,ndarray]:
    #     dConcatenatedOutput = self.weights.backward(inputs,error)
    #     dOutput = self._dOutput(dConcatenatedOutput)
    #     dScore = self._dScore(dOutput)

    #     dQuery = self._dQuery(dScore)
    #     dKey = self._dKey(dScore)
    #     dValue = self._dValue(dOutput)

    #     dQueries = self.weights_query.backward(inputs,dQuery).sum(axis=1,keepdims=True)
    #     dKeys = self.weights_keys.backward(inputs,dKey).sum(axis=1,keepdims=True)
    #     dValues = self.weights_values.backward(inputs,dValue).sum(axis=1,keepdims=True)        
    #     return dQueries,dKeys,dValues
    
    # def _dOutput(self, dConcatenatedOutput:ndarray) -> ndarray:
    #     return dConcatenatedOutput.reshape(-1,dConcatenatedOutput.shape[2],ModelSettings.N_HEADS.value,self.OUTPUT_DIMENSION).transpose(0,2,1,3)
    
    # def _dScore(self, dOutput:ndarray) -> ndarray:
    #     dScore = dOutput@self.values.transpose(0,1,3,2)
    #     dScore = self.softmax.backward(dScore)
    #     dScore *= sqrt(ModelSettings.HIDDEN_DIMENSION.value)
    #     return dScore
    
    # def _dValue(self, dOutput:ndarray) -> ndarray:
    #     return self.scores.transpose(0,1,3,2) @ dOutput

    # def _dQuery(self, dScore:ndarray) -> ndarray:
    #     return dScore @ self.keys
    
    # def _dKey(self, dScore:ndarray) -> ndarray:
    #     return dScore.transpose(0,1,-1,-2) @ self.queries

    # @staticmethod
    # def _scaled_scores(queries:ndarray, keys:ndarray) -> ndarray:
    #     scores = queries @ keys.transpose(0,1,-1,-2) 
    #     scores /= sqrt(ModelSettings.HIDDEN_DIMENSION.value) 
    #     return scores

    # @staticmethod
    # def _mask(shape:tuple) -> ndarray:
    #     return tile(triu(ones(shape[-1],shape[-1]),1) * ModelSettings.ATTENTION_MASK_CONSTANT.value,(shape[0],shape[1],1,1))
