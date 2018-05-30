import mahotas as mh
import networkx as nx
import numpy as np
import gabolFilter
import cv2
import matplotlib.pyplot as plt


cells = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


def minutiae_at(pixels, i, j):
    if pixels[i][j] == 0:
        return "none"

    values = [int(pixels[i + k][j + l]) for k, l in cells]
    # print(values)

    crossings = 0
    for k in range(0, 8):
        crossings += abs(values[k] - values[k + 1])
    crossings = int(crossings / 2)

    if crossings == 1:
        return "ending"
    if crossings == 3:
        return "bifurcation"
    return "bifurcation"

cellsxy = [(0, 0), (1, 0),  (0, 1), (1, 1)]
def minutiae_at_p(pixels, i, j):
    result = minutiae_at(pixels, i, j)
    if result == "ending" or result == "none":
        return result

    values = [int(pixels[i + k][j + l]) for k, l in cellsxy]
    #

    crossings = abs(values[0] + values[1] + values[2] + values[3])
    # print(crossings)

    if crossings > 2:
        return "cross"

    return result


def toGraph(imagearray):
    (yLen, xLen) = imagearray.shape

    result = np.ones((xLen, yLen), np.uint8)
    result = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
    cv2.rectangle(result, (0, 0), (xLen, yLen), (255, 255, 255), -1)


    G = nx.Graph()
    tmparray = []
    index = 0
    for i in range(1, xLen - 1):
        for j in range(1, yLen - 1):
            minutiae = minutiae_at_p(imagearray, i, j)
            if minutiae != "none":
                if minutiae == "ending":
                    cv2.circle(result, (i, j), 10, (0, 0, 150))
                elif minutiae == "cross":
                    # tmparray.append(tmp)
                    G.add_node((i,j))
                    index +=1
                    cv2.circle(result, (i, j), 10, (0, 150, 0), -1)
                else:
                # elif minutiae == "bifurcation":
                    cv2.line(result, (i, j), (i + 1, j + 1), (150, 0, 0))
    # for i in range(1, xLen - 1):
    #     for j in range(1, yLen - 1):
    #         minutiae = minutiae_at(imagearray, i, j)
    #         if minutiae != "none":
    #             if minutiae == "ending":
    #                 # G.add_node()
    #                 cv2.circle(result,(i,j),10,(0,0,150))
    #             elif minutiae == "cross":
    #                 cv2.circle(result,(i,j),2,(0,150,0),-1)
    #             elif minutiae == "bifurcation" :
    #                 cv2.line(result,(i,j),(i+1,j+1),(150,0,0))
    cv2.imwrite("image/wwwsde.png", result)
    return G

def draw(graph):
    plt.subplot(2, 1, 1)
    plt.title("insan")
    nx.draw(graph, node_size=10)
    plt.show()

if __name__ == "__main__":
    src = cv2.imread("image/www.png", cv2.THRESH_BINARY)
    binaryimage = gabolFilter._floodfill(src)
    Bgraph = toGraph(binaryimage)
    draw(Bgraph)

    # cv2.imshow("Bgraph", cv2.resize(Bgraph, (600, 600)))
    # cv2.waitKey()
    # cv2.imwrite("image/wwwsd.png", Bgraph)
    # (xLen, yLen) = src.shape
    # print(xLen, yLen)
# skeletonB = mh.thin(src)
# Bgraph = C8skeleton_to_graph(skeletonB)
# cv2.imshow("Bgraph", cv2.resize(Bgraph, (600, 600)))

# skeletonH = mh.thin(imH)
# Hgraph = C8skeleton_to_graph(skeletonH)

# figsize(6, 6)
# subplot(221, xticks=[]
#         , yticks=[])
# imshow(imB, interpolation='nearest')
# subplot(222, xticks=[], yticks=[])
# nx.draw(Bgraph)
# subplot(223, xticks=[], yticks=[])
# imshow(imH, interpolation='nearest')
# subplot(224, xticks=[], yticks=[])
# nx.draw(Hgraph)