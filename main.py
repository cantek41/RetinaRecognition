from Similarty.FactorySimilarity import SimilarityFactory, SIMILARITY
import cv2
from ImageToGraph import guo_hall_Thinning, utility
import networkx as nx


def createGraph():
    src = cv2.imread("image/www.png", cv2.THRESH_BINARY)
    graph = guo_hall_Thinning.prop(src)
    img = utility.draw_graph(src, graph)
    cv2.imshow("Bgraph", cv2.resize(img, (600, 600)))
    cv2.imwrite("image/graphh.png", img)
    nx.write_gml(graph, "graph.gml")
    return graph

def similarty(graph):
    print("size : ", graph.number_of_nodes())
    print("==========================================")
    similartyEigenvector = SimilarityFactory.create(SIMILARITY.Eigenvector, graph, graph)
    print("Eigenvector benzerlik oranı", similartyEigenvector.getSimilarity())

    print("==========================================")
    similartyCos = SimilarityFactory.create(SIMILARITY.Cosinus, graph, graph)
    print("Cos benzerlik oranı", similartyCos.getSimilarity())
    # cv2.waitKey()


if __name__ == "__main__":
    print("Başlıyor...")
    G = createGraph()
    # G = nx.read_gml('graph.gml')
    similarty(G)


