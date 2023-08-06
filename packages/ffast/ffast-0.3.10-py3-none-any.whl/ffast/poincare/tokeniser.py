from typing import List, Generator

from nltk.util import ngrams
from numpy import zeros, ndarray, argmax, full

from ffast.poincare.token import Token
from ffast.poincare.tokens import Tokens
from ffast.poincare.utils import Poincare, PREPROCESSOR, VOCABULARY, VECTORS, SIZE_SENTENCE_VECTOR

class Tokeniser:
    def __init__(self) -> None:
        self.size = SIZE_SENTENCE_VECTOR
        self.token_size = Poincare.SIZE_VECTOR.value
        self.special_tokens = list()

    def __len__(self) -> int:
        return Poincare.SIZE_VOCABULARY.value + len(self.special_tokens) + 1
    
    def add_special_token(self, token:str) -> None:
        if token not in self.special_tokens and token not in VOCABULARY:
            self.special_tokens.append(token)
            self.special_tokens.sort()

    def encode(self, text:str) -> Tokens:
        return Tokens(self._tokenise(text),pad_token_id=len(self)-1)
    
    def decode(self, ids:List[int]) -> Tokens:
        return Tokens(list(self._convert_ids_to_tokens(ids)),pad_token_id=len(self)-1)
    
    def _tokenise(self, text:str) -> List[Token]:
        unknown_token_id = len(self)-1
        words = text.split()
        number_of_words = len(words)
        tokens = [None]*number_of_words
        for ngram_size in range(number_of_words+1,0,-1):
            for index_start,ngram in enumerate(ngrams(words,ngram_size)):
                index_end = index_start + ngram_size
                if any(tokens[index_start:index_end]):
                    continue 
                raw_token = ' '.join(words[index_start:index_end])
                normalised_token = PREPROCESSOR.normalise(text=' '.join(ngram))
                if normalised_token in self.special_tokens:
                    id = Poincare.SIZE_VOCABULARY.value + self.special_tokens.index(normalised_token)
                    vector = full(Poincare.SIZE_VECTOR.value,-1)
                elif raw_token in VOCABULARY:
                    id = VOCABULARY.index(raw_token)
                    vector = VECTORS[id]
                elif normalised_token in VOCABULARY:
                    id = VOCABULARY.index(normalised_token)
                    vector = VECTORS[id]
                else:
                    id = unknown_token_id
                    vector = zeros(Poincare.SIZE_VECTOR.value)
                    normalised_token = Poincare.UNKNOWN.value
                if id != unknown_token_id or ngram_size==1:
                    tokens[index_start:index_end] = [Poincare.SKIP.value]*ngram_size
                    tokens[index_start] = Token(
                        raw_token=raw_token,
                        normalised_token=normalised_token,
                        vector = vector,
                        id = id
                    )
        return list(filter(lambda token:isinstance(token,Token),tokens))

    def _convert_ids_to_tokens(self, ids:List[int]) -> Generator[Token,None,None]:
        for id in ids:
            if id < Poincare.SIZE_VOCABULARY.value:
                token = VOCABULARY[id]
                vector = VECTORS[id]
            else:
                id_special_token = id - Poincare.SIZE_VOCABULARY.value
                if id_special_token < len(self.special_tokens):
                    token = self.special_tokens[id_special_token] 
                else:
                    token = Poincare.UNKNOWN.value
                vector= zeros(Poincare.SIZE_VECTOR.value)
            yield Token(
                raw_token=token,
                normalised_token=token,
                vector = vector,
                id = id
            )

    @staticmethod
    def decode_semantics(poincare_vectors:List[ndarray]) -> Tokens:
        return Tokeniser.decode(ids=map(Tokeniser._convert_semantics_to_token_id,poincare_vectors))

    @staticmethod
    def _convert_semantics_to_token_id(semantics:ndarray) -> int:
        return argmax(VECTORS @ semantics)