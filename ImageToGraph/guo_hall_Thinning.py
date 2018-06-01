import cv2
import networkx as nx
import numpy as np
from collections import defaultdict
from itertools import chain
from ImageToGraph import gabolFilter, ToGraph
import matplotlib.pyplot as plt

class AlgBody():
    def __init__(self):
        self.name = "Guo Hall Graph Detection"
        self.parent = "Graph Detection"
        self.result = {"img": None, "graph": None, "skeleton": None}
    def process(self, args):
        # create a skeleton
        skeleton = args[2]
        image = args[0]
        # detect nodes
        # graph = zhang_suen_node_detection(skeleton)
        graph = ToGraph.toGraph(skeleton)
        # detect edges
        # graph = breadth_first_edge_detection(skeleton, gray_img, graph)
        graph = breadth_first_edge_detection(skeleton, image, graph)
        #skeleton = cv2.cvtColor(skeleton, cv2.COLOR_GRAY2BGR)
        self.result['graph'] = graph
        self.result['img'] = image

def breadth_first_edge_detection(skel, segmented, graph):
    def neighbors(x, y):
        item = skel.item
        width, height = skel.shape
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                # the line below is ugly and is intended to be this way
                # do not try to modify it unless you know what you're doing
                if (dx != 0 or dy != 0) and \
                                        0 <= x + dx < width and \
                                        0 <= y + dy < height and \
                                item(x + dx, y + dy):
                    yield x + dx, y + dy

    def distance_transform_diameter(edge_trace, segmented):
        dt = cv2.distanceTransform(segmented, 2, 0)
        edge_pixels = np.nonzero(edge_trace)
        diameters = defaultdict(list)
        for label, diam in zip(edge_trace[edge_pixels], 2.0 * dt[edge_pixels]):
            diameters[label].append(diam)
        return diameters

    label_node = dict()
    queues = []
    label = 1
    label_length = defaultdict(int)
    for x, y in graph.nodes_iter():
        for a, b in neighbors(x, y):
            label_node[label] = (x, y)
            label_length[label] = 1.414214 if abs(x - a) == 1 and \
                                              abs(y - b) == 1 else 1
            queues.append((label, (x, y), [(a, b)]))
            label += 1

    edges = set()
    edge_trace = np.zeros(skel.shape, np.uint32)
    edge_value = edge_trace.item
    edge_set_value = edge_trace.itemset
    label_histogram = defaultdict(int)

    while queues:
        new_queues = []
        for label, (px, py), nbs in queues:
            for (ix, iy) in nbs:
                value = edge_value(ix, iy)
                if value == 0:
                    edge_set_value((ix, iy), label)
                    label_histogram[label] += 1
                    label_length[label] += 1.414214 if abs(ix - px) == 1 and \
                                                       abs(iy - py) == 1 else 1
                    new_queues.append((label, (ix, iy), neighbors(ix, iy)))
                elif value != label:
                    edges.add((min(label, value), max(label, value)))
        queues = new_queues

    diameters = distance_transform_diameter(edge_trace, segmented)
    for l1, l2 in edges:
        u, v = label_node[l1], label_node[l2]
        if u == v:
            continue
        d1, d2 = diameters[l1], diameters[l2]
        diam = np.fromiter(chain(d1, d2), np.uint, len(d1) + len(d2))
        graph.add_edge(u, v, pixels=label_histogram[l1] + label_histogram[l2],
                       length=label_length[l1] + label_length[l2],
                       width=np.mean(diam),
                       width_var=np.var(diam))
    return graph

def draw(graph):
    plt.subplot(2, 1, 1)
    plt.title("graph")
    nx.draw(graph, node_size=10)
    plt.show()

def prop(src):
    binaryimage = gabolFilter._floodfill(src)
    data = [src, "", binaryimage]
    alg = AlgBody()
    alg.process(data)
    return alg.result['graph']

if __name__ == '__main__':
    src = cv2.imread("../image/www.png", cv2.THRESH_BINARY)
    grap = prop(src)
    draw(grap)

