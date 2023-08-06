from typing import List

from jellyfish import metaphone 
from numpy import ndarray, array, argmax

from ffast.poincare.utils import Poincare

class Token:
    def __init__(self, raw_token:str, normalised_token:str, vector:ndarray, id:int) -> None:
        self.text = raw_token
        self.morphology = normalised_token
        self.phonology = metaphone(raw_token)
        self.semantics = vector
        self.id = id

    def __repr__(self) -> str:
        return f"""
        text = {self.text}
        morphology = {self.morphology}
        phonology = {self.phonology}
        id = {self.id}
        """

    def __str__(self) -> str:
        return self.text 

    def most_similar(self, others:List["Token"]) -> "Token":
        others_vectors = array(list(map(lambda other:other.semantics, others)))
        index_best = argmax(others_vectors@self.semantics)
        return others[index_best]