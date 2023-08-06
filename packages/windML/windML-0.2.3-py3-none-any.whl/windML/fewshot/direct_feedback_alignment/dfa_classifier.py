from typing import Tuple, List, Optional
from scipy.special import expit
from pathlib import Path

from numpy import mean, ndarray, sum, newaxis, power, arccos, clip, pi, argmax, array, tanh, zeros, savetxt, loadtxt
from numpy.random import randn, permutation, seed
from numpy.linalg import norm

from windML.fewshot.direct_feedback_alignment.utils import ModelSettings
from windML.utils.classifier import Classifier

class DFAClassifier(Classifier):
    """
    Feedforward Neural Network Classifier
    trained using Direct Feedback Alignment or Back Propagation
    """
    def __init__(self, input_dimension:int, output_dimension:int, load_path:Optional[str]=None, direct_feedback_alignment:bool=True) -> None:
        self.direct_feedback_alignment = direct_feedback_alignment
        if load_path is None:
            self.LABELS = list()
            self.weights1 = randn(ModelSettings.HIDDEN_DIMENSION.value, input_dimension)
            self.weights2 = randn(output_dimension, ModelSettings.HIDDEN_DIMENSION.value)
        else:
            self.LABELS = loadtxt(f"{load_path}/LABELS.txt",dtype=str)
            self.weights1 = loadtxt(f"{load_path}/weights1.txt")
            self.weights2 = loadtxt(f"{load_path}/weights2.txt")
        if self.direct_feedback_alignment:
            seed(0)
            self.random_weights = randn(ModelSettings.HIDDEN_DIMENSION.value, output_dimension)
    
    def labels(self) -> List[str]:
        return self.LABELS

    def predict(self, input:ndarray) -> ndarray:
        return self._predict_batch(array([input]).T).T[0]

    def _predict_batch(self, inputs:ndarray) -> ndarray:
        return self._forward_pass(array(inputs))
    
    def classify(self, input:ndarray) -> List[str]:
        id = argmax(self.predict(input))
        return self.LABELS[id]

    def save(self,name:str) -> str:
        path = f"{Path.cwd()}/{name}"
        Path(path).mkdir(parents=True, exist_ok=True)
        savetxt(f"{path}/LABELS.txt",self.LABELS,fmt="%s")
        savetxt(f"{path}/weights1.txt",self.weights1)
        savetxt(f"{path}/weights2.txt",self.weights2)

    def train_autoencoder(self, train_inputs:List[ndarray], train_labels:List[str]) -> None:
        self.LABELS = sorted(set(train_labels))
        x = array(train_inputs).T
        y = array(self._one_hot_encode_batch(train_labels,self.LABELS)).T
        self.fit(x,y)

    def fit(self, train_inputs:ndarray, train_outputs:ndarray) -> Tuple[List[float],List[float]]:        
        _,dataset_size = train_inputs.shape
        n_batches = dataset_size//ModelSettings.BATCH.value

        training_error,angles = list(),list()
        for epoch in range(ModelSettings.EPOCHS.value):
            train_inputs_shuffled,train_outputs_shuffled = self._shuffle_data(dataset_size, train_inputs,train_outputs)
            error,angle = self._partial_fit(n_batches,train_inputs_shuffled,train_outputs_shuffled)
            training_error.append(error/dataset_size)
            angles.append(angle)
            print(f'\nLoss at epoch {epoch+1}: Training error: {training_error[-1]}%')
        return training_error,angles

    def _backward_pass(self, error:ndarray, inputs:ndarray) -> None:
        self.weights2 += self._dWeights(error, self.final_hidden)
        error_activation = self._dActivation(error)     
        self.weights1 += self._dWeights(error_activation, inputs)

    def _partial_fit(self,n_batches:int, train_inputs:ndarray,train_outputs:ndarray) -> Tuple[float,float]:
        error,angle = 0.,0.
        for batch in range(n_batches):
            train_inputs_sampled,train_outputs_sampled = self._sample_data(batch,train_inputs,train_outputs)
            e,angle = self._fit_batch(train_inputs_sampled, train_outputs_sampled)
            error += e
            print(f"\rbatch: {batch} - {100*round(batch/n_batches,2)}%",end="")
        return error, angle

    def _fit_batch(self, train_inputs:ndarray, train_outputs:ndarray) -> Tuple[float,float]:
        predicted_output_logits = self._forward_pass(train_inputs)
        self._backward_pass(
            error=predicted_output_logits - train_outputs, 
            inputs=train_inputs
        )
        return (
            self._train_error(predicted_output_logits,train_outputs),
            self._average_angle(predicted_output_logits - train_outputs) if self.direct_feedback_alignment else 0
        )

    def _average_angle(self, error:ndarray) -> float:
        c = self._c(error)        
        dHidden =  self._dHidden(error)
        Lk = self._Lk(dHidden, c) 
        return self._angle(Lk, c)
        
    def _dActivation(self,error:ndarray) -> ndarray:
        e = self.random_weights @ error if self.direct_feedback_alignment else self.weights2.T @ error
        return e *  ( 1 - tanh(self.activation1)**2 )

    def _dHidden(self, error:ndarray) -> ndarray:
        return mean( self.random_weights @ error , axis=1)[:, newaxis]

    def _c(self, error:ndarray) -> ndarray:
        activationInverse = expit( self.activation2 ) 
        activationInverseMultInverse = 1 - activationInverse
        a = activationInverse * activationInverseMultInverse
        e = error * a
        return mean( self.weights2.T @ e, axis=1)[:, newaxis]

    def _first_half_forward_pass(self, inputs:ndarray) -> ndarray:
        self.activation1 = self._project(
            inputs=inputs,
            weights=self.weights1,
        )
        return tanh(self.activation1)

    def _last_half_forward_pass(self,inputs:ndarray) -> ndarray:
        self.activation2 = self._project(
            inputs=inputs,
            weights=self.weights2,
        )
        return expit(self.activation2)
    
    def _forward_pass(self, inputs:ndarray) -> ndarray:
        self.final_hidden = self._first_half_forward_pass(inputs)
        return self._last_half_forward_pass(self.final_hidden)
        
    @staticmethod
    def _dWeights(error:ndarray, inputs:ndarray) -> ndarray:
        dWeights = -error @ inputs.T 
        return ModelSettings.LEARNING_RATE.value * dWeights

    @staticmethod
    def _angle(Lk:ndarray, c:ndarray) -> float:
        return arccos(clip(Lk*DFAClassifier._inverse(c), -1., 1.)) * 180/pi

    @staticmethod
    def _Lk(dHidden:ndarray, c:ndarray) -> ndarray:
        return ((dHidden.T @ c) * DFAClassifier._inverse(dHidden))[0, 0]

    @staticmethod
    def _project(inputs:ndarray, weights:ndarray) -> ndarray: 
        return weights @ inputs 
    
    @staticmethod
    def _inverse(x:ndarray) -> ndarray:
        return power(norm(x), -1)

    @staticmethod
    def _shuffle_data(dataset_size:int, train_inputs:ndarray, train_outputs:ndarray) -> Tuple[ndarray,ndarray]:
        shuffled_ids = permutation(dataset_size)
        return train_inputs[:, shuffled_ids], train_outputs[:, shuffled_ids]

    @staticmethod
    def _sample_data(batch_number:int, train_inputs_shuffled:ndarray, train_outputs_shuffled:ndarray) -> Tuple[ndarray,ndarray]:
        return (
            train_inputs_shuffled[:, batch_number*ModelSettings.BATCH.value:(batch_number+1)*ModelSettings.BATCH.value],
            train_outputs_shuffled[:, batch_number*ModelSettings.BATCH.value:(batch_number+1)*ModelSettings.BATCH.value]
        )

    @staticmethod
    def _train_error(predicted:ndarray, expected:ndarray) -> int:
        return sum(argmax(predicted, axis=0) != argmax(expected, axis=0))

    @staticmethod
    def _one_hot_encode_batch(targets:List[str],labels:List[str]) -> List[ndarray]:
        vector_size = len(labels)
        return list(map(lambda target: DFAClassifier._one_hot_encode(labels.index(target),vector_size),targets))
    
    @staticmethod
    def _one_hot_encode(index:int, vector_size:int) -> ndarray:
        vector = zeros(vector_size)
        vector[index] = 1
        return vector