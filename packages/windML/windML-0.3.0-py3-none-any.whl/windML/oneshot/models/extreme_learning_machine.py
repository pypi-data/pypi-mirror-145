from typing import Optional, List
from pathlib import Path

from numpy import ndarray, exp, savetxt, loadtxt, argmax
from numpy.linalg import pinv
from numpy.random import uniform, seed

from windML.utils.label_encoding import one_hot_encode_batch

class ELMClassifier:
    """
    Extreme Learning Machine
    """
    def __init__(self, input_dimension:int, hidden_dimension:int=1000, load_path:Optional[str]=None) -> None:
        seed(0)
        self.random_projection = uniform(
            low=-.1, high=.1, 
            size =(input_dimension, hidden_dimension)
        )
        if load_path is None:
            self.LABELS = list()
            self.weights = None
        else:
            self.LABELS = loadtxt(f"{load_path}/LABELS.txt",dtype=str)
            self.weights = loadtxt(f"{load_path}/weights.txt")

    def fit(self, inputs: List[ndarray], labels: List[int]) -> None:
        self.LABELS = sorted(set(labels))
        label_vectors = one_hot_encode_batch(labels,self.LABELS)
        hidden = self._hidden_layer(inputs)
        self.weights = self._learn_dense_weights(hidden, label_vectors)

    def save(self, name:str) -> str:
        path = f"{Path.cwd()}/{name}"
        Path(path).mkdir(parents=True, exist_ok=True)
        savetxt(f"{path}/LABELS.txt",self.LABELS,fmt="%s")
        savetxt(f"{path}/weights.txt",self.weights)

    def predict(self, inputs: ndarray) -> ndarray:
        return self._output_layer(self._hidden_layer(inputs))
    
    def classify(self, inputs: ndarray) -> str:
        class_id = argmax(self.predict(inputs))
        return self.LABELS[class_id]

    def _hidden_layer(self, inputs: ndarray) -> ndarray: 
        return self.activation_function(inputs @ self.random_projection)
  
    def _output_layer(self, hidden: ndarray) -> ndarray: 
        return hidden @ self.weights
    
    def _learn_dense_weights(self, hidden:ndarray, label_vectors:List[ndarray]) -> ndarray:
        return pinv(hidden) @ label_vectors

    @staticmethod
    def activation_function(x: ndarray) -> ndarray: 
        return ELMClassifier.sigmoid(x)
    
    @staticmethod
    def sigmoid(x: ndarray) -> ndarray:
        return 1. / (1. + exp(-x))