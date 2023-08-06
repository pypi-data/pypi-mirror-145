from pathlib import Path
from typing import Optional

from numpy import zeros, ndarray, eye, zeros, savetxt, loadtxt, exp, sqrt
from numpy.random import random, seed
from numpy.linalg import pinv, inv
from numpy.linalg.linalg import LinAlgError


from windML.oneshot.models.utils import ModelSettings 

class RecurrentELM:
    def __init__(self, input_dimension:ndarray, output_dimension:ndarray, load_path:Optional[str]=None) -> None:
        seed(0)
        self.bias = random((1, ModelSettings.HIDDEN_DIMENSION.value)) * 2 - 1

        self.input_weights  = random((ModelSettings.HIDDEN_DIMENSION.value, input_dimension)) *2 -1
        self.hidden_weights = random((ModelSettings.HIDDEN_DIMENSION.value, ModelSettings.HIDDEN_DIMENSION.value))
        if load_path is None:
            self.output_weights = zeros((ModelSettings.HIDDEN_DIMENSION.value, output_dimension))
        else:
            self.output_weights = loadtxt(f"{load_path}/output_weights.txt")

        self.hidden_state = random((1, ModelSettings.HIDDEN_DIMENSION.value)) * 2 -1
        self.M = inv(ModelSettings.WEIGHT_FACTOR.value * eye(ModelSettings.HIDDEN_DIMENSION.value))

    def save(self, name:str) -> None:
        path = f"{Path.cwd()}/{name}"
        Path(path).mkdir(parents=True, exist_ok=True)
        savetxt(f"{path}/output_weights.txt",self.output_weights)

    def fit(self, inputs:ndarray, targets:ndarray) -> None:
        batch_size, _ = targets.shape
        hidden_state = self._hidden_layer(inputs)
        try:
            self._fit_M(hidden_state, batch_size)
            self._fit_output_weights(hidden_state,targets)
        except LinAlgError:
            pass

    def forward(self, inputs:ndarray) -> ndarray:
        hidden_state = self._hidden_layer(inputs)
        return self._output_layer(hidden_state)

    def _output_layer(self, hidden_state:ndarray) -> ndarray:
        return hidden_state @ self.output_weights

    def _hidden_layer(self, inputs:ndarray) -> ndarray:
        logits = self.linear_recurrent(
            inputs=inputs,
            hidden=self.hidden_state,
            input_weights=self.input_weights,
            hidden_weights=self.hidden_weights,
            bias= self.bias
        )
        normalised_logits = self.normalisation_layer(logits)
        self.hidden_state = self.sigmoid(normalised_logits)
        return self.hidden_state

    def _fit_M(self, hidden_state:ndarray, batch_size:int) -> None:
        projected_hidden = hidden_state @ self.M
        projected_hidden_inverse = self.M @ hidden_state.T
        pseudoinverse_state = pinv(eye(batch_size) + hidden_state @ projected_hidden_inverse)
        projected_pseudoinverse = pseudoinverse_state @ projected_hidden
        inverse_projected_pseudoinverse = hidden_state.T @ projected_pseudoinverse
        self.M -= self.M @ inverse_projected_pseudoinverse

    def _fit_output_weights(self, hidden_state:ndarray, targets:ndarray) -> None:
        output_errors = targets - self._output_layer(hidden_state)
        hidden_errors = hidden_state.T @ output_errors
        output_weight_errors = self.M @ hidden_errors
        self.output_weights += output_weight_errors

    @staticmethod
    def linear_recurrent(inputs:ndarray, input_weights:ndarray, hidden_weights:ndarray, hidden:ndarray, bias:ndarray) -> ndarray:
        projected_inputs = inputs @ input_weights.T
        projected_hidden = hidden @ hidden_weights
        return projected_inputs + projected_hidden + bias
    
    @staticmethod
    def sigmoid(inputs:ndarray) -> ndarray:
        return 1 / ( 1 + exp(-inputs))

    @staticmethod
    def normalisation_layer(inputs:ndarray) -> ndarray:
        inputs_variance = inputs-inputs.mean()
        inputs_variance_positive = sqrt(inputs.var() + ModelSettings.NORMALISATION_FACTOR.value)
        return inputs_variance/inputs_variance_positive