from string import punctuation

from nltk.stem import WordNetLemmatizer
from unidecode import unidecode

class PreprocessingPipeline:
    def __init__(self) -> None:
        self.lemmatiser = WordNetLemmatizer()
        self.TRANSLATION_TABLE = "".maketrans(punctuation, " " * len(punctuation))

    def preprocess(self, text:str) -> str:
        lowercase_text = text.lower()
        unaccented_text = unidecode(lowercase_text)
        unpunctuated_text = unaccented_text.translate(self.TRANSLATION_TABLE)
        return unpunctuated_text

    def normalise(self, text:str) -> str:
        text = self.preprocess(text)
        for delimiter in "-_":
            text = text.replace(delimiter," ")
        return ' '.join(map(self.lemmatiser.lemmatize,text.split()))
