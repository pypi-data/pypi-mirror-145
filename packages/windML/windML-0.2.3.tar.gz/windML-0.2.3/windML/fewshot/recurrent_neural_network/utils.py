from enum import Enum 
from string import punctuation

VOCABULARY = " 0123456789abcdefghijklmnopqrstuvwxyz" + punctuation

class ModelSettings(Enum):
    VOCABULARY_SIZE = len(VOCABULARY)    
    HIDDEN_DIMENSION = 100 
    EPOCHS = 1000
    SEQUENCE_LENGTH = 30
    LEARNING_RATE = 1e-3
    WEIGHT_SCALE_FACTOR = 1e-2
    OVERFLOW_LIMIT = 5
    ADAGRAD = 1e-8
    BOS_TOKEN = "$"
    EOS_TOKEN = "~"
    PAD_TOKEN = " "