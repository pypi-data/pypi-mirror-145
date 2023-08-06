from lib2to3.pgen2 import token
from numpy.random import randint

from windML.fewshot.transformer.model import Transformer
from windML.fewshot.transformer.utils import ModelSettings

model = Transformer()

token_ids = randint(3, size=(2, ModelSettings.SEQUENCE_LENGTH.value, ModelSettings.VOCABULARY_SIZE.value))
print(token_ids)
predictions = model.forward(token_ids[0,:,:], token_ids[1,:,:])
print(predictions)