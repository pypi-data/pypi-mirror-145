from typing import List, Generator, Optional
from functools import reduce 

from numpy import ndarray, concatenate, argmax, array, zeros, pad

from ffast.wordnet.token import Token
from ffast.wordnet.utils import (
    WordNet, METAPHONES, VOCABULARY,
    SIZE_SEMANTIC_VECTOR, SIZE_METAPHONES
)

class Tokens:
    def __init__(self, tokens:List[Token]) -> None:
        self.tokens = tokens
        self.__pointer = -1
        self.ids = list(map(lambda token:token.id,self))
        self.vector = self.__sentence_embedding() if any(tokens) else None

    def __repr__(self) -> str:
        return '\n'.join(map(repr,self.tokens))
    
    def __str__(self) -> str:
        return ' '.join(map(str,self.tokens))

    def __len__(self) -> int:
        return len(self.tokens)

    def __iter__(self) -> "Tokens":
        return self
    
    def __next__(self) -> Token: 
        self.__pointer += 1
        if self.__pointer < len(self):
            return self.tokens[self.__pointer]
        raise StopIteration
    
    def __getitem__(self,index:int) -> Token:
        return self.tokens[index]

    def __round__(self, n:int) -> ndarray:
        return pad(self.ids, pad_width=(0,n))[:n]

    def skip_unknowns(self) -> "Tokens":
        return Tokens(list(filter(lambda token:token.tag != WordNet.UNKNOWN.value,self.tokens)))

    def skip_stopwords(self) -> "Tokens":
        return Tokens(list(filter(lambda token:token.tag != WordNet.STOPWORD.value,self.tokens)))
    
    def nouns(self) -> "Tokens":
        return Tokens(list(filter(lambda token:token.tag == WordNet.POS_NOUN.value, self.tokens)))

    def verbs(self) -> "Tokens":
        return Tokens(list(filter(lambda token:token.tag == WordNet.POS_VERB.value, self.tokens)))

    def entities(self) -> "Tokens":
        return Tokens(list(filter(lambda token:token.tag in (WordNet.POS_VERB.value,WordNet.POS_NOUN.value,WordNet.UNKNOWN.value,WordNet.SPECIAL.value), self.tokens)))

    def paraphrase(self) -> Generator[str, None, None]:
        for index,token in enumerate(self.tokens):
            for similar_token in token.similar_tokens:
                yield f"{' '.join(map(str,self.tokens[:index]))} {similar_token} {' '.join(map(str,self.tokens[index+1:]))}"
        yield str(self)

    def most_similar(self, others:List["Tokens"]) -> Optional["Tokens"]:
        if self.vector is None:
            return None
        others_with_vectors = filter(lambda other:other.vector is not None,others)
        others_vectors = array(list(map(
            lambda other:other.vector, 
            others_with_vectors
        )))
        index_best = argmax(others_vectors@self.vector)
        return others[index_best]

    def __sentence_embedding(self) -> ndarray:
        sparse_token_vectors = list(map(self.__embed_token,self.tokens))
        return concatenate([
            reduce(lambda vector1,vector2: vector1 & vector2, sparse_token_vectors),
            reduce(lambda vector1,vector2: vector1 | vector2, sparse_token_vectors),
            reduce(lambda vector1,vector2: vector1 ^ vector2, sparse_token_vectors),
        ])
        
    @staticmethod
    def __embed_token_phonetics(token:Token) -> ndarray:
        embedding = zeros(SIZE_METAPHONES,dtype=int)
        for character in token.phonology:
            metaphone_index = METAPHONES.index(character)
            embedding[metaphone_index] = 1
        return embedding

    @staticmethod
    def __embed_token_semantics(token:Token) -> ndarray:
        embedding = zeros(SIZE_SEMANTIC_VECTOR,dtype=int)
        if token.id >= SIZE_SEMANTIC_VECTOR:
            return embedding
        embedding[token.id] = 1
        for name in token.semantics:
            relation_index = VOCABULARY.index(name)
            embedding[relation_index] = 1
        return embedding
        
    @staticmethod
    def __embed_token(token:Token) -> ndarray:
        return concatenate([
            Tokens.__embed_token_phonetics(token),
            Tokens.__embed_token_semantics(token),
        ])    