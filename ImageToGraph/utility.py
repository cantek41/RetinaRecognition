import cv2
import numpy
from ImageToGraph import guo_hall_Thinning

NODESIZESCALING = 750
EDGETRANSPARENCYDIVIDER = 5
EDGETRANSPARENCY = False


def draw_graph(image, graph):
    tmp = draw_edges(image, graph)
    node_size = int(numpy.ceil((max(image.shape) / float(NODESIZESCALING))))
    return draw_nodes(tmp, graph, max(node_size, 1))


def draw_nodes(img, graph, radius=1):
    for x, y in graph.nodes_iter():
        cv2.circle(img, (y - radius, x - radius), 10,
                   (0, 150, 0), -1)
    return img


def draw_edges(img, graph, col=(0, 0, 255)):
    (yLen, xLen) = img.shape

    edg_img = numpy.zeros((xLen, yLen), numpy.uint8)

    max_standard_deviation = 0
    if EDGETRANSPARENCY:
        max_standard_deviation = find_max_edge_deviation(graph)

    for (x1, y1), (x2, y2) in graph.edges_iter():
        start = (y1, x1)
        end = (y2, x2)
        diam = graph[(x1, y1)][(x2, y2)]['width']
        width_var = graph[(x1, y1)][(x2, y2)]['width_var']
        standard_dev = numpy.sqrt(width_var)
        if diam == -1: diam = 2
        diam = int(round(diam))
        if diam > 255:
            diam = 255
        if EDGETRANSPARENCY:
            edge_cur_standard_deviation = graph[(x1, y1)][(x2, y2)]['standard_deviation']
            opacity = edge_cur_standard_deviation / max_standard_deviation * 0.8
            (b, g, r) = col
            overlay = (0, 0 ,0) 
            target_col = (b == 0 if 0 else opacity * 255 + (1 - opacity) * b,
                          g == 0 if 0 else opacity * 255 + (1 - opacity) * g,
                          r == 0 if 0 else opacity * 255 + (1 - opacity) * r)
            cv2.line(edg_img, start, end, (150, 0, 0), 2)
        else:
            try:
                cv2.line(edg_img, start, end, (150, 0, 0), 2)
            except :
                print(start, end, col, diam)

    edg_img = cv2.addWeighted(img, 0.5, edg_img, 0.5, 0)
    MAXIMUMSTANDARDDEVIATION = 0
    return edg_img

def find_max_edge_deviation(graph):
    max_standard_deviation = 0
    for (x1, y1), (x2, y2) in graph.edges_iter():
        deviation = graph[(x1, y1)][(x2, y2)]['width_var']
        standard_deviation = numpy.sqrt(deviation)
        graph[(x1, y1)][(x2, y2)]['standard_deviation'] = standard_deviation

        if max_standard_deviation < standard_deviation:
            max_standard_deviation = standard_deviation

    return max_standard_deviation


if __name__ == '__main__':
    src = cv2.imread("../image/www.png", cv2.THRESH_BINARY)
    grap = guo_hall_Thinning.prop(src)
    img = draw_graph(src, grap)
    cv2.imshow("img", cv2.resize(img, (600, 600)))
    cv2.imwrite("../image/graphh.png", img)
    cv2.waitKey(0)


