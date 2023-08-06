from typing import List 

from numpy import zeros, ndarray

def one_hot_encode_batch(targets:List[str],labels:List[str]) -> List[ndarray]:
    vector_size = len(labels)
    return list(map(lambda target: one_hot_encode(labels.index(target),vector_size),targets))
    
def one_hot_encode(index:int, vector_size:int) -> ndarray:
    vector = zeros(vector_size,dtype=int)
    vector[index] = 1
    return vector
