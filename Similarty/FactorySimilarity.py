from enum import Enum
from Similarty.CosSimilarity import CosSim
from Similarty.Eigenvector import Eigenvector


class SIMILARITY(Enum):
    NbSimilarity = 0
    Cosinus = 1
    Eigenvector = 2


class SimilarityFactory():
    @staticmethod
    def create(similarity_type ,Garph1 ,Graph2):
        if similarity_type == SIMILARITY.Cosinus:
            return CosSim(Garph1, Graph2)
        elif similarity_type == SIMILARITY.Eigenvector:
            return Eigenvector(Garph1, Graph2)

