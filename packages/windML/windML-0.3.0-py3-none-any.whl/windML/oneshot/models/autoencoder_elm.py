from numpy import zeros,ndarray, eye, zeros
from numpy.random import random, seed
from numpy.linalg import pinv, inv
from numpy.linalg.linalg import LinAlgError

from windML.oneshot.models.utils import ModelSettings, sigmoid, normalisation_layer

class AutoencoderELM:
    def __init__(self, input_dimension:int, output_dimension:int) -> None:
        seed(0)
        self.input_weights = random((ModelSettings.HIDDEN_DIMENSION.value, input_dimension)) * 2 - 1
        self.output_weights = zeros((ModelSettings.HIDDEN_DIMENSION.value, output_dimension))
        self.bias = random((1, ModelSettings.HIDDEN_DIMENSION.value)) * 2 - 1
        self.activation_function = sigmoid 
        self.normalisation = normalisation_layer
        self.M = inv(ModelSettings.WEIGHT_FACTOR.value * eye(ModelSettings.HIDDEN_DIMENSION.value))

    def _output_layer(self, hidden_state:ndarray) -> ndarray:
        return hidden_state @ self.output_weights

    def _hidden_layer(self, inputs:ndarray) -> ndarray:
        logits = inputs @ self.input_weights.T 
        biased_logits = logits + self.bias 
        normalised_logits = self.normalisation(biased_logits)
        return self.activation_function(normalised_logits)

    def forward(self, inputs:ndarray) -> ndarray:
        hidden_state = self._hidden_layer(inputs)
        return hidden_state @ self.output_weights
        
    def fit(self, inputs:ndarray, targets:ndarray) -> None:
        batch_size, _ = targets.shape
        hidden_state = self._hidden_layer(inputs)
        try:
            self._fit_M(hidden_state, batch_size)
            self._fit_output_weights(hidden_state,targets)        
        except LinAlgError:
            pass

    def _fit_output_weights(self, hidden_state:ndarray, targets:ndarray) -> None:
        output_errors = targets - self._output_layer(hidden_state)
        hidden_errors = hidden_state.T @ output_errors
        output_weight_errors = self.M @ hidden_errors
        self.output_weights += output_weight_errors

    def _fit_M(self, hidden_state:ndarray, batch_size:int) -> None:
        projected_hidden = hidden_state @ self.M
        projected_hidden_inverse = self.M @ hidden_state.T
        pseudoinverse_state = pinv(eye(batch_size) + hidden_state @ projected_hidden_inverse)
        projected_pseudoinverse = pseudoinverse_state @ projected_hidden
        inverse_projected_pseudoinverse = hidden_state.T @ projected_pseudoinverse
        self.M -= self.M @ inverse_projected_pseudoinverse