import mahotas as mh
import networkx as nx
import numpy as np
import gabolFilter
import cv2
import matplotlib.pyplot as plt
def C8skeleton_to_graph(skeletonC8):
    # images processing: extraction of branchedpoints, end-points, edges
    ep = endPoints(skeletonC8)
    bp = branchedPoints(skeletonC8, showSE=False)
    ## Label branched-points
    l_bp, _ = mh.label(bp)
    ## Label the edges
    l_edges = edges_from_C8skel(skeletonC8)
    ##Make end-points with the same label than their edge
    l_ep = ep * l_edges

    ##edges between branched-points
    endpoints_labels = np.where(mh.histogram.fullhistogram(np.uint16(l_ep))[:] == 1)[0]
    edges_bp = np.copy(l_edges)
    for l in endpoints_labels:
        edges_bp[np.where(edges_bp == l)] = 0
    # edges between end-points and branched points
    edges_ep_to_bp = l_edges * np.logical_not(edges_bp > 0)

    # Building graph
    ## Add branched points first
    G = nx.Graph()
    lab_bpTonode = add_bp_to_graph(G, l_bp)
    ## Add end-points
    lab_epTonode = add_ep_to_graph(G, l_ep)
    ##Link end-points to branched-points
    ###labels of bp
    branchedpoints_labels = np.where(mh.histogram.fullhistogram(np.uint16(l_bp))[:] == 1)[0]
    for lab in branchedpoints_labels:
        pos = np.where(l_bp == lab)
        row = int(pos[0])
        col = int(pos[1])
        # search label(s) of edges in image containing edges between ep and bp
        ## first get the neighborhood of the curent bp
        neigh_epbp = edges_ep_to_bp[row - 1:row + 1 + 1, col - 1:col + 1 + 1]
        labels_in_neigh = np.where(mh.histogram.fullhistogram(np.uint16(neigh_epbp))[:] != 0)[0]
        # print neigh_epbp, labels_in_neigh[1:]
        # get node(s) of attribute label= labels_in_neigh ! may be more than one, think to a  list
        for lab_ep in labels_in_neigh[1:]:
            # search for nodes f attribute label= lab_ep
            w = np.sum(l_edges == lab_ep)
            print
            'linking ', lab, lab_ep, ' weight ', w
            G.add_edge(lab_bpTonode[lab], lab_epTonode[lab_ep], weight=w)  #
    ##
    ##Now try to link branched points between them
    ##
    bps_neighborhood = {}
    branchedpoints_labels = np.where(mh.histogram.fullhistogram(np.uint16(l_bp))[:] == 1)[0]
    for lab in branchedpoints_labels:
        pos = np.where(l_bp == lab)
        row = int(pos[0])
        col = int(pos[1])
        # search label(s) of edges in image containing edges between ep and bp
        ## first get the neighborhood of the curent bp
        neigh_epbp = edges_bp[row - 1:row + 1 + 1, col - 1:col + 1 + 1]
        labels_in_neigh = np.where(mh.histogram.fullhistogram(np.uint16(neigh_epbp))[:] != 0)[0]
        bps_neighborhood[lab] = labels_in_neigh[1:].tolist()
    print
    bps_neighborhood

    ## Build the dictionnary of edges see (http://stackoverflow.com/questions/21375146/pythonic-inverse-dict-non-unique-mappings)
    invert_is_edges = {item: [key for key in bps_neighborhood if item in bps_neighborhood[key]] for value in
                       bps_neighborhood.values() for item in value}
    ## Addeges to graph
    for ed in invert_is_edges.keys():
        ## first get edge size -> its weight
        w = np.sum(edges_bp == ed)
        vertex1 = invert_is_edges[ed][0]
        vertex2 = invert_is_edges[ed][1]
        # print ed,w
        G.add_edge(vertex1, vertex2, weight=w)
    ## This is it !!
    return

def draw(graph):
    plt.subplot(2, 1, 1)
    plt.title("insan")
    nx.draw(graph, node_size=10)
    plt.show()

src = cv2.imread("image/www.png", cv2.THRESH_BINARY)
binaryimage = gabolFilter._floodfill(src)
g=C8skeleton_to_graph(src)
draw(g)