import PiHarmoniousLabelingFinder as phlf
import matplotlib.pyplot as plt
import networkx as nx
import itertools as it

if __name__ == '__main__':
    test_graph = nx.windmill_graph(2,4)
    test_graph = nx.complete_multipartite_graph(1,3)
    test_graph.add_edge(1,4)
    u8 = [1, 3, 5, 7]
    u21 = [1, 2, 4, 5, 8, 10, 11, 13, 16, 17, 19, 20]
    u24 = [1, 5, 7, 11, 13, 17, 19, 23]
    u13 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    u33 = [1, 2, 4, 5, 7, 8, 10, 13, 14, 16, 17, 19, 20, 23, 25, 26, 28, 29, 31, 32]
    u15 = [1, 2, 4, 7, 8, 11, 13, 14]

    # labels = u13
    labels = u8
    mod = max(labels)+1

    print(f"labeling {nx.to_graph6_bytes(test_graph, header=False).strip()} with {labels} and mod {mod}")
    phlf.get_labeling(test_graph, labels, mod)