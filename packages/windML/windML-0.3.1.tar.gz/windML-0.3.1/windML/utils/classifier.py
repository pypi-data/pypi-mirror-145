from typing import List
from numpy import ndarray

class Classifier:
    def labels(self) -> List[str]:
        raise NotImplementedError

    def predict(self, inputs:ndarray) -> ndarray:
        raise NotImplementedError

    def classify(self, inputs:ndarray) -> List[str]:
        raise NotImplementedError
    
    def save(self, name:str) -> str:
        raise NotImplementedError
    
    def fit(self, inputs:List[ndarray], targets:List[int]) -> None:
        raise NotImplementedError
