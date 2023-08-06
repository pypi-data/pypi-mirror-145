from typing import List, Dict

from numpy import ndarray, add

from windML.fewshot.transformer.utils import ModelSettings
from windML.fewshot.transformer.layers.dense import DenseLayer
from windML.fewshot.transformer.layers.position_encoder import PositionEncodingLayer
from windML.fewshot.transformer.layers.multihead_attention import MultiHeadAttention
from windML.fewshot.transformer.layers.residual import ResidualLayer
from windML.fewshot.transformer.layers.dropout import DropoutLayer
from windML.fewshot.transformer.layers.normalisation import NormalisationLayer


class DecoderBlock:
    def __init__(self) -> None:
        self.positional_encoding_layer = PositionEncodingLayer() 
        self.multihead_attention1 = MultiHeadAttention()
        self.multihead_attention2 = MultiHeadAttention()
        self.residual_layer1 = ResidualLayer()
        self.residual_layer2 = ResidualLayer()
        self.residual_layer3 = ResidualLayer()
        self.dropout_layer1 = DropoutLayer()
        self.dropout_layer2 = DropoutLayer()
        self.dropout_layer3 = DropoutLayer()
        self.normalisation_layer1 = NormalisationLayer()
        self.normalisation_layer2 = NormalisationLayer()
        self.normalisation_layer3 = NormalisationLayer()

    def forward(self, context: ndarray, inputs: ndarray) -> ndarray:
        context = self.positional_encoding_layer.forward(context)        

        attention1 = self.multihead_attention1.forward(
            Q=self.deep_layers(context), 
            K=self.deep_layers(context), 
            V=self.deep_layers(context)
        )
        summed = add(context, attention1)
        residual1 = self.residual_layer1.forward(summed, output_dimension=summed.shape[-1])
        dropout1 = self.dropout_layer1.forward(residual1)
        normalised1 = self.normalisation_layer1.forward(dropout1)

        attention2 = self.multihead_attention2.forward(
            Q=self.deep_layers(context),
            K=self.deep_layers(inputs),
            V=self.deep_layers(inputs)
        )
        summed2 = add(normalised1, attention2)
        residual2 = self.residual_layer2.forward(summed2, output_dimension=summed2.shape[-1])
        dropout2 = self.dropout_layer2.forward(residual2)
        normalised2 = self.normalisation_layer2.forward(dropout2)

        residual3 = self.residual_layer3.forward(normalised2, output_dimension=normalised2.shape[-1])
        dropout3 = self.dropout_layer3.forward(residual3)
        normalised3 = self.normalisation_layer3.forward(dropout3)
        return normalised3

    @staticmethod
    def deep_layers(inputs:ndarray) -> List[callable]:
        return dict(map(
            lambda index:(index, DenseLayer().forward(inputs)),
            range(ModelSettings.N_HEADS.value)
        ))


    # def backward(self,inputs:ndarray,error:ndarray) -> Tuple[ndarray,ndarray]:
    #     dLayer3 = self.normalisation_layer3.backward(error)
    #     dLogits = self.dense_layer2.backward(inputs,dLayer3)
    #     dLogits[self.activations] = 0
    #     dNormLayer2 = self.dense_layer1.backward(inputs,dLogits) + dLayer3
    #     dLayer2 = self.normalisation_layer2.backward(dNormLayer2)        
    #     dNormLayer1, dNormLayer1Key, dNormLayer1Value = self.attention_layer2.backward(inputs,dLayer2)  
    #     dNormLayer1 += dLayer2
    #     dLayer1 = self.normalisation_layer1.backward(dNormLayer1)        
    #     dInput, dInputKey, dInputValue = self.attention_layer1.backward(inputs,dLayer1)        
    #     dInput = dInput + dInputKey + dInputValue + dLayer1
    #     dContext = dNormLayer1Key + dNormLayer1Value
    #     return dInput, dContext
