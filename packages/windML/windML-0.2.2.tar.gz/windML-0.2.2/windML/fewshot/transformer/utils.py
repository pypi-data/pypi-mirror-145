from enum import Enum 

class ModelSettings(Enum):
    SEQUENCE_LENGTH = 15
    EMBEDDING_DIMENSION = 128
    VOCABULARY_SIZE = 128
    N_HEADS = 8
    N_DECODERS = 8
    SCALING_FACTOR = .01
    DROPOUT_RATE = .2
    AVOID_DIVISION_BY_ZERO = 1e-5

assert ModelSettings.EMBEDDING_DIMENSION.value % ModelSettings.N_HEADS.value == 0