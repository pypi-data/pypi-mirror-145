from typing import Generator, Tuple
from enum import Enum 

from nltk.corpus import stopwords
from nltk.corpus.reader.wordnet import Synset
from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import ADJ, ADJ_SAT, ADV, NOUN, VERB

from ffast.preprocessor import PreprocessingPipeline

def create_vocabulary() -> Generator[Tuple[str,Synset],None,None]:
    for meaning in wordnet.all_synsets():
        for lemma in meaning.lemmas():
            yield (
                PREPROCESSOR.normalise(lemma.name()),
                meaning.name()
            )

PREPROCESSOR = PreprocessingPipeline()
STOPWORDS = sorted(stopwords.words('english'))
VOCABULARY_WORDNET = dict(create_vocabulary())
VOCABULARY = sorted(map(lambda meaning:meaning.name(),wordnet.all_synsets()))
SIZE_STOPWORDS = len(STOPWORDS)
SIZE_WORDNET = len(VOCABULARY)
METAPHONES = "ABCEFHIJKLMNOPRSTUWXY0. "
SIZE_METAPHONES = len(METAPHONES)
SIZE_SEMANTIC_VECTOR = SIZE_STOPWORDS + SIZE_WORDNET 
SIZE_WORD_VECTOR = SIZE_SEMANTIC_VECTOR + SIZE_METAPHONES 
SIZE_SENTENCE_VECTOR = 3*SIZE_WORD_VECTOR 

class WordNet(Enum):
    SKIP = "skip"
    UNKNOWN = "<Unknown>"
    SPECIAL = "<Special>"
    STOPWORD = "<StopWord>"
    POS_NOUN = "Noun"
    POS_VERB = "Verb"
    POS_MAP = {
        NOUN:"Noun",
        VERB:"Verb",
        ADV:"Adverb",
        ADJ:"Adjective",
        ADJ_SAT:"Adjective"
    }
    EXAMPLE_DELIMITER = "; "
    SYNSET_NAME_DELIMITER = "."