from typing import List, Tuple, Optional
from pathlib import Path

from numpy.random import randn, choice
from numpy import argmax, zeros, ndarray, copy, tanh, exp, sum, log, zeros_like, clip, sqrt, savetxt, loadtxt

from windML.fewshot.recurrent_neural_network.utils import ModelSettings
from windML.utils.label_encoding import one_hot_encode


class RNN:
    """
    Recurrent Neural Network (RNN)
    """
    def __init__(
        self, token_vector_size:int, token_vocabulary_size:int, 
        load_path:Optional[str]=None, hidden_dimension:int=ModelSettings.HIDDEN_DIMENSION.value
    ) -> None:
        self.input_dimension = token_vector_size
        self.output_dimension = token_vocabulary_size
        self.hidden_dimension = hidden_dimension   
        if load_path is None:
            self.weights1 = randn(hidden_dimension, self.input_dimension)*ModelSettings.WEIGHT_SCALE_FACTOR.value     
            self.weights2 = randn(hidden_dimension, hidden_dimension)*ModelSettings.WEIGHT_SCALE_FACTOR.value 
            self.weights3 = randn(self.output_dimension, hidden_dimension)*ModelSettings.WEIGHT_SCALE_FACTOR.value
            self.bias1 = zeros((hidden_dimension, 1)) 
            self.bias2 = zeros((self.output_dimension, 1)) 
        else:
            self.weights1 = loadtxt(f"{load_path}/weights1.txt")
            self.weights2 = loadtxt(f"{load_path}/weights2.txt")
            self.weights3 = loadtxt(f"{load_path}/weights3.txt")
            self.bias1 = loadtxt(f"{load_path}/bias1.txt")
            self.bias2 = loadtxt(f"{load_path}/bias2.txt")
            self.bias1 = self.bias1.reshape((self.bias1.shape[0],1))
            self.bias2 = self.bias2.reshape((self.bias2.shape[0],1))
    
    def save(self, name:str) -> None:
        path = f"{Path.cwd()}/{name}"
        Path(path).mkdir(parents=True, exist_ok=True)
        savetxt(f"{path}/weights1.txt",self.weights1)
        savetxt(f"{path}/weights2.txt",self.weights2)
        savetxt(f"{path}/weights3.txt",self.weights3)
        savetxt(f"{path}/bias1.txt",self.bias1)
        savetxt(f"{path}/bias2.txt",self.bias2)

    def generate(
        self, token_ids_vectoriser:callable, bos_id:int, eos_id:int, 
        prompt_ids:List[int], condition_vector:Optional[ndarray]=None, 
        generation_length:int=ModelSettings.SEQUENCE_LENGTH.value, greedy:bool=True
    ) -> List[int]:
        if condition_vector is None:
            hidden_context = self._new_hidden_context()
        else: 
            assert condition_vector.shape == (self.hidden_dimension,1)
            hidden_context = condition_vector 

        token_ids = [bos_id] + prompt_ids
        encoded_inputs = token_ids_vectoriser(token_ids)
        for encoded_input in encoded_inputs:
            hidden_context = self._hidden_state(encoded_input,hidden_context)

        for _ in range(generation_length):            
            encoded_input = token_ids_vectoriser([token_ids[-1]])[0]
            hidden_context = self._hidden_state(encoded_input,hidden_context)
            logits = self._logits(hidden_context)
            index = self._choose_index_greedily(logits) if greedy else self._choose_index_stochastically(self.output_dimension, logits)
            if index == eos_id:
                break
            token_ids.append(index)

        return token_ids

    def fit(
        self, token_ids_vectoriser:callable, token_ids:List[List[int]], 
        encoded_contexts:Optional[List[ndarray]]=None, epochs:int=ModelSettings.EPOCHS.value
    ) -> None:
        encoded_inputs = list(map(token_ids_vectoriser,token_ids))
        if encoded_contexts is None:
            encoded_contexts = list(map(lambda _:None,encoded_inputs))
        else:
            assert encoded_contexts[0].shape == (self.hidden_dimension,1)
        mWeights1 = zeros_like(self.weights1)
        mWeights2 = zeros_like(self.weights2)
        mWeights3 = zeros_like(self.weights3)
        mBias1 = zeros_like(self.bias1)
        mBias2 = zeros_like(self.bias2) 

        for epoch in range(epochs):
            for context,inputs,targets in zip(encoded_contexts,encoded_inputs,token_ids):
                inputs = inputs[:-1]
                targets = targets[1:]                
                loss = self._forward_pass(inputs, targets, context)
                self._update_parameters(
                    parameters=(self.weights1, self.weights2, self.weights3, self.bias1, self.bias2),
                    dParameters=self._backward_pass(inputs, targets),
                    mParameters=(mWeights1, mWeights2, mWeights3, mBias1, mBias2)
                )            
            print(f'epoch {epoch} / {epochs} [loss = {loss}]') 

    def _forward_pass(self, inputs:List[ndarray], targets:List[int], context_vector:Optional[ndarray]=None) -> float:        
        self.inputs = dict()
        self.probabilities = dict()        
        self.hiddens = dict()
        self.hiddens[-1] = self._new_hidden_context() if context_vector is None else context_vector

        loss = 0
        for position,encoded_input in enumerate(inputs): 
            hidden_state = self._hidden_state(encoded_input, self.hiddens[position-1])
            logits = self._logits(hidden_state)
            probability = self.softmax(logits) 
            loss += self.cross_entropy(probability,targets[position])
            self.inputs[position] = encoded_input
            self.hiddens[position] = hidden_state
            self.probabilities[position] = probability
        return loss

    def _backward_pass(self, inputs:List[ndarray], targets:List[int]) -> Tuple[ndarray,ndarray,ndarray,ndarray,ndarray]:
        dWeights1 = zeros_like(self.weights1)
        dWeights2 = zeros_like(self.weights2)
        dWeights3 = zeros_like(self.weights3) 
        dBias1 =  zeros_like(self.bias1)
        dBias2 = zeros_like(self.bias2)
        dHiddenContext = self._new_hidden_context()

        for position in reversed(range(len(inputs))):
            dTarget = self._dTarget(targets[position], self.probabilities[position])
            dWeights3 += self._dWeights3(dTarget,self.hiddens[position])
            dBias2 += dTarget 
            dHidden = self._dHidden(dTarget,dHiddenContext)
            dInput = self._dInput(self.hiddens[position], dHidden)
            dBias1 += dInput
            dWeights1 += self._dWeights1(self.inputs[position], dInput)
            dWeights2 += self._dWeights2(self.hiddens[position-1], dInput)
            dHiddenContext = self._dHiddenContext(dInput)

        for value in [dWeights1, dWeights2, dWeights3, dBias1, dBias2]: 
            clip(value, -ModelSettings.OVERFLOW_LIMIT.value, ModelSettings.OVERFLOW_LIMIT.value, out=value)
        return dWeights1,dWeights2,dWeights3,dBias1,dBias2
    
    def _hidden_state(self, input:ndarray, prior_hidden_state:ndarray) -> ndarray:
        return tanh(
            (self.weights1 @ input) + 
            (self.weights2 @ prior_hidden_state) + 
            self.bias1
        )

    def _logits(self, hidden_state:ndarray) -> ndarray:
        return self.weights3 @ hidden_state + self.bias2

    def _dHidden(self, dTarget:ndarray, dHiddenContext:ndarray) -> ndarray:
        return self.weights3.T @ dTarget + dHiddenContext

    def _dHiddenContext(self, dInput:ndarray) -> ndarray:
        return self.weights2.T @ dInput

    def _new_hidden_context(self) -> ndarray:
        return zeros((self.hidden_dimension,1)) 

    @staticmethod
    def cross_entropy(probability:ndarray, target:ndarray) -> float:
        return -log(probability[target,0]) 

    @staticmethod
    def softmax(x:float) -> float:
        e = exp(x)
        return e / sum(e) 

    @staticmethod
    def _dTarget(target:ndarray, probability:ndarray) -> ndarray:
        dTarget = copy(probability) 
        dTarget[target] -= 1 
        return dTarget

    @staticmethod
    def _dWeights3(dTarget:ndarray, hidden_state:ndarray) -> ndarray:
        return dTarget @ hidden_state.T

    @staticmethod
    def _dInput(hidden_state:ndarray, dHidden:ndarray) -> ndarray:
        return (1 - hidden_state ** 2 ) * dHidden

    @staticmethod
    def _dWeights1(input:ndarray, dInput:ndarray) -> ndarray:
        return dInput @ input.T

    @staticmethod
    def _dWeights2(prior_hidden_state:ndarray, dInput:ndarray) -> ndarray:
        return dInput @ prior_hidden_state.T

    @staticmethod
    def _update_parameters(
        parameters:Tuple[ndarray,ndarray,ndarray,ndarray,ndarray],
        dParameters:Tuple[ndarray,ndarray,ndarray,ndarray,ndarray],
        mParameters:Tuple[ndarray,ndarray,ndarray,ndarray,ndarray]
    ) -> None:
        for value, dValue, mValue in zip(parameters, dParameters, mParameters):
            mValue += dValue * dValue 
            value -= ModelSettings.LEARNING_RATE.value * dValue / sqrt(mValue + ModelSettings.ADAGRAD.value)     

    @staticmethod
    def _choose_index_stochastically(vocabulary_size:int, logits:ndarray) -> int:
        return choice(
            a=range(vocabulary_size), 
            p=RNN.softmax(logits).ravel()
        ) 

    @staticmethod
    def _choose_index_greedily(logits:ndarray) -> int:
        return argmax(logits)