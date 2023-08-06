from typing import List, Generator, Optional, Set

from ffast.wordnet.utils import (
    WordNet, VOCABULARY, STOPWORDS,
    SIZE_STOPWORDS, SIZE_WORDNET
)

from nltk.corpus.reader.wordnet import Synset
from nltk.wsd import lesk
from nltk.corpus import wordnet
from jellyfish import metaphone 

class Token:
    def __init__(
        self, raw_token:str, normalised_token:str, 
        synset_name:Optional[str],SPECIAL_TOKENS:Optional[List[str]],
        sense_disambiguation_context:Optional[str]=None
    ) -> None:
        self.text = raw_token 
        self.morphology = normalised_token
        self.phonology = metaphone(raw_token)
        self.similar_tokens = set()
        self.opposite_tokens = set()
        self.related_tokens = set()
        self.semantics = set()
        self.definition = None
        self.example = None
        if raw_token in SPECIAL_TOKENS:
            self.id = SIZE_WORDNET + SIZE_STOPWORDS + SPECIAL_TOKENS.index(raw_token)
            self.tag = WordNet.SPECIAL.value
        elif normalised_token in STOPWORDS: 
            self.id = SIZE_WORDNET + STOPWORDS.index(normalised_token)
            self.tag = WordNet.STOPWORD.value            
        elif synset_name is None:
            self.id = SIZE_WORDNET + SIZE_STOPWORDS + 1
            self.tag = WordNet.UNKNOWN.value 
        else:
            if sense_disambiguation_context is None:
                meaning = wordnet.synset(synset_name)
                self.id = VOCABULARY.index(synset_name)
            else:
                meaning = lesk(sense_disambiguation_context.split(),synset_name.split(WordNet.SYNSET_NAME_DELIMITER.value)[0])
                self.id = VOCABULARY.index(meaning.name())
            self.tag = WordNet.POS_MAP.value.get(meaning.pos())
            self.similar_tokens = self.synonyms(normalised_token,meaning)
            self.opposite_tokens = set(self.antonyms(meaning))
            self.related_tokens = self._related_to(meaning)
            self.semantics = self.synset_lineage(meaning)
            self.definition = meaning.definition()
            self.example = WordNet.EXAMPLE_DELIMITER.value.join(meaning.examples())

    def __repr__(self) -> str:
        return f"""
        text = {self.text}
        morphology = {self.morphology}
        phonology = {self.phonology}
        id = {self.id}
        tag = {self.tag}
        similar = {self.similar_tokens}
        opposite = {self.opposite_tokens}
        related = {self.related_tokens}
        semantics = {self.semantics}
        definition = {self.definition}
        example = {self.example}
        """

    def __str__(self) -> str:
        return self.text 
        
    def _related_to(self, meaning:Synset) -> Set[str]:
        return set(self._remove_duplicates(
            values=self._get_related_meanings(meaning),
            duplicates={self.morphology} | self.similar_tokens
        ))

    def _similarity(self, other:"Token") -> int:
        return len(
            self.semantics.intersection(other.semantics)
        ) + len(
            self.similar_tokens.intersection(other.similar_tokens)
        ) + len(
            self.related_tokens.intersection(other.related_tokens)
        ) + len(
            set(self.phonology).intersection(other.phonology)
        ) + int(self.id == other.id) + int(self.tag==other.tag)
    
    def most_similar(self, others:List["Token"]) -> "Token":
        scores = list(map(self._similarity, others))
        max_score = max(scores)
        index_best = scores.index(max_score)
        return others[index_best]

    @staticmethod
    def synset_lineage(meaning:Synset) -> Set[str]:
        return set(map(
            lambda parent:parent.name(), 
            meaning.closure(lambda parent:parent.hypernyms())
        ))

    @staticmethod
    def synonyms(token:str, meaning:Synset) -> Set[str]:
        return set(Token._remove_duplicates(
            values=meaning.lemma_names(),
            duplicates={token}
        ))

    @staticmethod
    def antonyms(meaning:Synset) -> Generator[str,None,None]:
        for name in meaning.lemmas():
            for antonym_meaning in name.antonyms():
                yield antonym_meaning.name()

    @staticmethod
    def _get_related_meanings(meaning:Synset) -> Generator[str,None,None]:
        for related_meanings in (
            meaning.hyponyms(),
            meaning.part_meronyms(),
            meaning.substance_meronyms(),
            meaning.member_meronyms(),
            meaning.part_holonyms(),
            meaning.substance_holonyms(),
            meaning.member_holonyms(),
            meaning.topic_domains(),
            meaning.region_domains(),
            meaning.usage_domains(),
            meaning.entailments(),
            meaning.causes(),
            meaning.also_sees(),
            meaning.verb_groups(),
            meaning.similar_tos()
        ):
            for related_meaning in related_meanings:
                for name in related_meaning.lemma_names():
                    yield name

    @staticmethod
    def _remove_duplicates(values:List[str],duplicates:Set[str]) -> Generator[str,None,None]:
        for value in set(values):
            if value not in duplicates:
                yield value