from typing import List, Generator

from nltk.util import ngrams

from ffast.wordnet.tokens import Token, Tokens
from ffast.wordnet.utils import (
    WordNet, PREPROCESSOR, 
    VOCABULARY, VOCABULARY_WORDNET, STOPWORDS,
    SIZE_STOPWORDS, SIZE_WORDNET, SIZE_SENTENCE_VECTOR
)
    
class Tokeniser:
    def __init__(self) -> None:
        self.size = SIZE_SENTENCE_VECTOR
        self.special_tokens = list()

    def __len__(self) -> int:
        return SIZE_WORDNET + SIZE_STOPWORDS + len(self.special_tokens) + 1

    def add_special_token(self, token:str) -> None:
        if token not in self.special_tokens and token not in VOCABULARY_WORDNET and token not in STOPWORDS:
            self.special_tokens.append(token)
            self.special_tokens.sort()

    def encode(self, text:str) -> Tokens:
        return Tokens(self._tokenise(text))

    def decode(self, ids:List[int]) -> Tokens:
        return Tokens(list(self._convert_ids_to_tokens(ids)))

    def _tokenise(self, text:str) -> List[Token]:
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
                synset_name = VOCABULARY_WORDNET.get(normalised_token)
                if synset_name is not None or ngram_size==1:
                    tokens[index_start:index_end] = [WordNet.SKIP.value]*ngram_size
                    tokens[index_start] = Token(
                        raw_token=raw_token,
                        normalised_token=normalised_token,
                        synset_name=synset_name,
                        sense_disambiguation_context=text,
                        SPECIAL_TOKENS=self.special_tokens
                    )
        return list(filter(lambda token:isinstance(token,Token),tokens))

    def _convert_ids_to_tokens(self, ids:List[int]) -> Generator[Token,None,None]:
        for id in ids:
            if id < SIZE_WORDNET:
                synset_name = VOCABULARY[id] 
                token = synset_name.split(WordNet.SYNSET_NAME_DELIMITER.value)[0]
            elif id < SIZE_WORDNET + SIZE_STOPWORDS:
                synset_name= None
                token = STOPWORDS[id-SIZE_WORDNET]
            elif id < SIZE_WORDNET + SIZE_STOPWORDS + len(self.special_tokens):
                synset_name= None
                id_special_token = id - (SIZE_WORDNET+SIZE_STOPWORDS)
                token = self.special_tokens[id_special_token] 
            else:
                synset_name= None
                token = WordNet.UNKNOWN.value                    
            yield Token(
                raw_token=token,
                normalised_token=PREPROCESSOR.preprocess(token),
                synset_name=synset_name,
                SPECIAL_TOKENS=self.special_tokens
            )