import networkx as nx
import numpy as np


def select_k(spectrum, minimum_energy=0.9):
    running_total = 0.0
    total = np.sum(spectrum)
    if total == 0.0:
        return len(spectrum)
    for i in range(len(spectrum)):
        running_total += spectrum[i]
        if running_total / total >= minimum_energy:
            return i + 1
    return len(spectrum)

class Eigenvector():

    def __init__(self, graph1, graph2):
        self.graph1 = graph1.to_undirected()
        self.graph2 = graph2.to_undirected()

    def _Similarity(self, list1, list2):
       pass

    def getSimilarity(self):
        laplacian1 = nx.laplacian_spectrum(self.graph1)
        laplacian2 = nx.laplacian_spectrum(self.graph2)
        k1 = select_k(laplacian1)
        k2 = select_k(laplacian2)
        k = min(k1, k2)
        similarity = sum((laplacian1[:k] - laplacian2[:k]) ** 2)
        if similarity == 0:
            similarity = 1
        return similarity

if __name__ == "__main__":
    G1 = nx.DiGraph()
    G1.add_edges_from([(1, 2), (2, 1), (1, 3), (4, 1), (2, 3), (3, 2), (4, 3)])

    G2 = nx.DiGraph()
    G2.add_edges_from([(1, 4), (1, 3), (3, 1), (6, 1), (6, 4), (6, 3), (3, 6), (2, 4), (2, 6), (3, 5)])
    # nsim = nsim_hs03(G1, G1)
    nbsimilarity = Eigenvector(G1.to_undirected(), G2.to_undirected())
    print(nbsimilarity.getSimilarity())



