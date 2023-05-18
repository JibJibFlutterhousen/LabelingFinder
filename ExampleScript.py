import networkx as nx

import LabelingFinder as lf

def graceful_comibine(item_1, item_2):
    return abs(item_1-item_2)

def z14_combine(item_1, item_2):
    return (item_1 + item_2) % 14

def z4xz2_combine(item_1, item_2):
    return (item_1[0] + item_2[0]) % 4, (item_1[1] + item_2[1]) % 2

def u13_combine(item_1, item_2):
    return (item_1 * item_2) % 13

if __name__ == '__main__':

    ##################################################
    #                                                #
    #               Graceful                         #
    #                                                #
    ##################################################

    # Graceful labeling of C_7 with Z_7 \cup {0}

    graph = nx.cycle_graph(7)
    z7_plus_0 = lf.graceful_set(7)

    # The following three variables, test_graph, labeling_set, and combine_function need to be overwritten to change the graph, vertex labeling set, and the way to combine elements of the vertex labeling set
    test_graph = graph
    labeling_set = z7_plus_0
    combine_function = graceful_comibine

    # Now we can find the vertex labeling

    vertex_labeling = lf.labeling_finder(test_graph, labeling_set, combine_function)

    # The following just shows a picture of the graph, labeling vertices and edges if appropriate
    
    layout = nx.kamada_kawai_layout(test_graph)

    if vertex_labeling is not None:
        print("Displaying C_7 gracefully labeled with { 0, 1, 2, 3, 4, 5, 6, 7 }")
        lf.draw_labeling(test_graph, vertex_labeling, combine_function)
    else:
        print("There are no valid labelings")

    ##################################################
    #                                                #
    #               Harmonious                       #
    #                                                #
    ##################################################

    # Harmonious labeling of the 2-ballanced tree with height 3 with Z_14

    graph = nx.balanced_tree(2,3)
    z14 = lf.harmonious_set(14)

    # The following three variables, test_graph, labeling_set, and combine_function need to be overwritten to change the graph, vertex labeling set, and the way to combine elements of the vertex labeling set
    test_graph = graph
    labeling_set = z14
    combine_function = z14_combine
    
    # Now we can find the vertex labeling

    vertex_labeling = lf.labeling_finder(test_graph, labeling_set, combine_function)

    # The following just shows a picture of the graph, labeling vertices and edges if appropriate
    
    layout = nx.kamada_kawai_layout(test_graph)

    if vertex_labeling is not None:
        print("Displaying 2-ballanced tree with height 3 harmoniously labeled with { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14 }")
        lf.draw_labeling(test_graph, vertex_labeling, combine_function)
    else:
        print("There are no valid labelings")

    ##################################################
    #                                                #
    #               Gamma-harmonious                 #
    #                                                #
    ##################################################

    # Gamma-harmonious labeling of C_8 with Z_4 x Z_2:

    graph = nx.cycle_graph(8)
    z4xz2 = lf.gamma_set(4,2)

    # The following three variables, test_graph, labeling_set, and combine_function need to be overwritten to change the graph, vertex labeling set, and the way to combine elements of the vertex labeling set
    test_graph = graph
    labeling_set = z4xz2
    combine_function = z4xz2_combine

    # Now we can find the vertex labeling

    vertex_labeling = lf.labeling_finder(test_graph, labeling_set, combine_function)

    # The following just shows a picture of the graph, labeling vertices and edges if appropriate
    
    layout = nx.kamada_kawai_layout(test_graph)

    if vertex_labeling is not None:
        print("Displaying C_8 Gamma harmoniously labeled with { (0,0), (0,1), (1,0), (1,1), (2,0), (2,1), (3,0), (3,1) }")
        lf.draw_labeling(test_graph, vertex_labeling, combine_function)
    else:
        print("There are no valid labelings")

    ##################################################
    #                                                #
    #               Pi-harmonious                    #
    #                                                #
    ##################################################

    # Pi-harmonious labeling of K_4 snake with U(13):

    graph = nx.windmill_graph(2,4)
    u13 = lf.pi_set(13)

    # The following three variables, test_graph, labeling_set, and combine_function need to be overwritten to change the graph, vertex labeling set, and the way to combine elements of the vertex labeling set
    test_graph = graph
    labeling_set = u13
    combine_function = u13_combine

    # Now we can find the vertex labeling

    vertex_labeling = lf.labeling_finder(test_graph, labeling_set, combine_function)

    # The following just shows a picture of the graph, labeling vertices and edges if appropriate
    
    layout = nx.kamada_kawai_layout(test_graph)

    if vertex_labeling is not None:
        print("Displaying K_4 snake Pi harmoniously wiht { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13 }")
        lf.draw_labeling(test_graph, vertex_labeling, combine_function)
    else:
        print("There are no valid labelings")