from typing import List, Optional
from pathlib import Path

from numpy import ndarray, array, argmax, savetxt, loadtxt
from numpy.linalg import pinv 

from windML.utils.classifier import Classifier
from windML.utils.label_encoding import one_hot_encode_batch

class MFRClassifier(Classifier):
    """
    Matrix Factorisation
    Retrieval-based classifier
    """
    def __init__(self,load_path:Optional[str]=None) -> None:
        if load_path is None:
            self.LABELS = list()
            self.label_vectors = None
        else:
            self.LABELS = loadtxt(f"{load_path}/LABELS.txt",dtype=str)
            self.label_vectors = loadtxt(f"{load_path}/label_vectors.txt") 

    def predict(self, input:ndarray) -> ndarray:
        return input @ self.label_vectors

    def classify(self, input:ndarray) -> str:
        label_id = argmax(self.predict(input))
        return self.LABELS[label_id]

    def fit(self, inputs:List[ndarray], labels:List[str]) -> None:
        self.LABELS = sorted(set(labels))
        self.label_vectors = self._matrix_factorisation(
            input_vectors=inputs,
            output_vectors_one_hot=one_hot_encode_batch(labels,self.LABELS),
        )

    def save(self,name:str) -> str:
        path = f"{Path.cwd()}/{name}"
        Path(path).mkdir(parents=True, exist_ok=True)
        savetxt(f"{path}/LABELS.txt",self.LABELS,fmt="%s")
        savetxt(f"{path}/label_vectors.txt",self.label_vectors)

    @staticmethod 
    def _matrix_factorisation(input_vectors:List[ndarray], output_vectors_one_hot:List[ndarray]) -> ndarray:    
        return pinv(input_vectors) @ array(output_vectors_one_hot)