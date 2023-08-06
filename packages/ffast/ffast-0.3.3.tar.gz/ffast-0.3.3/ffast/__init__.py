__version__ = "0.3.3"
WORDNET = "wordnet"
POINCARE = "poincare"

def load(vectors:str=WORDNET):
    if vectors==WORDNET:
        from ffast.wordnet.tokeniser import Tokeniser
        from nltk import download
        download(WORDNET)
        download('stopwords')
        return Tokeniser()
    if vectors==POINCARE:
        from ffast.poincare.tokeniser import Tokeniser
        return Tokeniser()    
    raise TypeError(f"{vectors} is an unrecognised choice. Valid choices are: '{WORDNET}' or '{POINCARE}'")