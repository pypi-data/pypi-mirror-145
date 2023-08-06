from numpy import ndarray, exp, max, broadcast_to
from numpy.random import randint

from windML.fewshot.transformer.decoder_block import DecoderBlock
from windML.fewshot.transformer.utils import ModelSettings

class Transformer:
    def __init__(self) -> None: 
        self.decoder_stack = list(map(lambda _: DecoderBlock(),range(ModelSettings.N_DECODERS.value)))
        self.weights = randint(2, size=(ModelSettings.EMBEDDING_DIMENSION.value * ModelSettings.SEQUENCE_LENGTH.value, ModelSettings.VOCABULARY_SIZE.value)) * ModelSettings.SCALING_FACTOR.value
        self.bias = randint(2, size=(ModelSettings.VOCABULARY_SIZE.value))

    def forward(self, context:ndarray, inputs:ndarray) -> ndarray:
        for decoder in self.decoder_stack:
            inputs = decoder.forward(inputs, context)
        outputs = self.dense_layer(inputs.flatten())
        return self.softmax(outputs)

    def dense_layer(self, inputs: ndarray) -> ndarray:        
        outputs = inputs @ self.weights 
        outputs += broadcast_to(self.bias, outputs.shape)
        return Transformer.sigmoid(outputs) 
  
    @staticmethod
    def sigmoid(inputs:ndarray) -> ndarray:
        return 1/(1 + exp(-inputs))  

    @staticmethod
    def softmax(inputs: ndarray) -> ndarray:
        e = exp(inputs - max(inputs))
        return e / e.sum(axis=-1)