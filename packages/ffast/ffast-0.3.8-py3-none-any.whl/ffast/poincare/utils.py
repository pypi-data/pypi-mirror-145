from enum import Enum
from pathlib import Path 

from numpy import loadtxt

from ffast.preprocessor import PreprocessingPipeline

PREPROCESSOR = PreprocessingPipeline()
METAPHONES = "ABCEFHIJKLMNOPRSTUWXY0. "
SIZE_METAPHONES = len(METAPHONES)
PATH = Path(__file__).parent/"poincare.txt"
raw_vocab = loadtxt(PATH,usecols=0,dtype=str)
VOCABULARY = list(map(PREPROCESSOR.normalise,raw_vocab))
VECTORS = loadtxt(PATH,usecols=range(1,101))

class Poincare(Enum):
    SIZE_VECTOR = 100
    SIZE_VOCABULARY = len(VOCABULARY)
    UNKNOWN = "<Unknown>"
    SKIP = "skip"

SIZE_TOKEN_VECTOR = Poincare.SIZE_VECTOR.value + SIZE_METAPHONES
SIZE_POWER_MEANS_VECTOR = 5*SIZE_TOKEN_VECTOR
SIZE_SENTENCE_VECTOR = 2*SIZE_POWER_MEANS_VECTOR