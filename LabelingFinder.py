import math
import multiprocessing

import networkx as nx
import itertools as it
import matplotlib.pyplot as plt

def _chunkerator(Iterator, Chunk_size):

    # We will be building up the list of values inside the values list
    values = list()

    # For each item in the iterator we assign it a number
    for number, item in enumerate(Iterator):

        # If values has Chunk_size items, then we can yield values then clear it out
        if len(values) >= Chunk_size:
            yield values
            values = list()

        # Then we add another item to the values list
        values.append(item)

    # If we've looped through each item in the iterator, but have some leftover values, then we yield those values as well
    if len(values) > 0:
        yield values

def _parallel_check_for_boolean(Function, Searching_for, Arguments, Chunk_size=5000000):
    
    # Set up the iterator that returns chunks of the input work
    work_generator = _chunkerator(Arguments, Chunk_size)

    # Parallelization is done with a multiprocessing pool
    with multiprocessing.Pool() as pool:

        # Keep working until all pieces of work have been done
        done = False
        while not done:

            # If there is work still to do
            try:
                part_work = iter(next(work_generator))
            except StopIteration as e:

                # When work_generator has no more chunks of work then the loop is done, this is handled by setting the flag variable and 
                done = True
                continue

            # For each function call with a set of arguments, if the boolean we're searching for is found, then we can short circuit and return
            for truth_value, output in pool.starmap(Function, part_work):
                if truth_value == Searching_for:
                    done = True
                    break

    # If the entire work is exhausted without finding Searching_for, then we can return the last pair of input and output
    return truth_value, output

def edge_injective(Graph, Node_label_list, Combine_function):
    
    # Because we will be working in parallel, we make our own copy of a dictionary of node labels
    node_label_dict = {item[0]:item[1] for item in zip(Graph.nodes(), Node_label_list)}
    
    # We then calculate the edge labels for each edge in the graph
    edge_labels = {edge:Combine_function(node_label_dict[edge[0]], node_label_dict[edge[1]]) for edge in Graph.edges()}

    # If there edge repetitions, the set will contain fewer elements than the number of edges
    if len(set(edge_labels.values())) == Graph.number_of_edges():
        return True
    else:
        return False
    
def _edge_injective_wrapper(Graph, Node_label_list, Combine_function):

    # This is a wrapper function that returns the truth value, as well as the valuable input argument that was sent to the edge_injective function
    return edge_injective(Graph, Node_label_list, Combine_function), Node_label_list

def _tree_labeling_set_iterator(Labeling_set):

    # We first pick a node label to repeat
    for repeated_node in Labeling_set:

        # We then permute the labeling set and add it to the repeated node, yielding the result
        for non_repeated_nodes in it.permutations(Labeling_set):
            temp_labeling_set = [repeated_node,]
            temp_labeling_set.extend(non_repeated_nodes)
            yield temp_labeling_set


def labeling_finder(Graph, Labeling_set, Combine_function):

    # First, we will be setting up iterators that contain positional arguments for _edge_injective_wrapper
        # argument_1 contains the graph
        # argument_2 contains the vertex labeling
        # argument_3 contains the function that can combine vertex labels

    # In the case that the graph is a tree, we need to allow a repeated edge label, this is done by way of using _tree_labeling_set_iterator 
    if nx.is_tree(Graph):
        argument_1 = (item[0] for item in it.zip_longest((Graph,), _tree_labeling_set_iterator(Labeling_set), fillvalue=Graph))
        argument_2 = _tree_labeling_set_iterator(Labeling_set)
        argument_3 = (item[0] for item in it.zip_longest((Combine_function,), _tree_labeling_set_iterator(Labeling_set), fillvalue=Combine_function))

    # Otherwise we only allow permutations of the vertex set 
    else:
        argument_1 = (item[0] for item in it.zip_longest((Graph,), it.permutations(Labeling_set, Graph.number_of_nodes()), fillvalue=Graph))
        argument_2 = it.permutations(Labeling_set, Graph.number_of_nodes())
        argument_3 = (item[0] for item in it.zip_longest((Combine_function,), it.permutations(Labeling_set, Graph.number_of_nodes()), fillvalue=Combine_function))
    
    # We can then put the positional arguments together into a single iterator
    arguments = zip(argument_1, argument_2, argument_3)
    
    # Now we use a parallelized search to check if any of the vertex label assignments results in an injective edge labeling
    truth_value, labeling_list = _parallel_check_for_boolean(_edge_injective_wrapper, True, arguments)
    
    # If we find a valid vertex labeling, we return it, otherwise we return None
    if truth_value:
        return {item[0]:item[1] for item in zip(Graph.nodes(), labeling_list)}
    else:
        return None

def draw_labeling(Graph, Vertex_labeling, Combine_function):

    # This facilitates the drawing of the supplied graph with the supplied vertex labels and the induced edge labels according to the supplied Combine_function
    
    # First fix the drawing orientation
    layout = nx.kamada_kawai_layout(Graph)

    # Calculate the induced edge labels
    edge_label_dict = {edge:Combine_function(Vertex_labeling[edge[0]], Vertex_labeling[edge[1]]) for edge in Graph.edges()}
    
    # Draw the graph nodes, edges, and vertex labels
    nx.draw(Graph, 
            pos=layout,
            with_labels=True,
            labels=Vertex_labeling,
            font_color="black",
            edge_color="lightgrey",
            node_color="lightgrey")

    # Draw the edge labels
    nx.draw_networkx_edge_labels(Graph,
                                pos=layout,
                                edge_labels=edge_label_dict)
    
    # Display the created image
    plt.show()

def graceful_set(n):
    # This returns the closed set of integers [0,n]
    # 
    # For example graceful_set(3) returns Z_3 = { 1, 2, 3 }
    return [x for x in range(0,n+1,1)]

def harmonious_set(n):
    # This returns the closed set of integers [1,n]
    # 
    # For example harmonious_set(3) returns Z_3 \cup {0} = { 0, 1, 2, 3 }
    return [x for x in range(1,n+1,1)]

def gamma_set(*args):
    # This returns the direct product of Z_n for each n given as arguments
    # 
    # For example gamma_set(3,2) returns Z_3 x Z_2 = { (0,0), (1,0), (2,0), (1,0), (1,1), (2,1) }
    labels = list([(item,) for item in range(args[0])])
    for index,mod in enumerate(args[1:]):
        for item in [label for label in labels if len(label) == index+1]:
            [labels.append(item+(new_item,)) for new_item in range(mod)]
    remove_items = [item for item in labels if len(item) < len(args)]
    [labels.remove(item) for item in remove_items]
    return tuple(labels)

def pi_set(n):
    # This returns the closed set of positive integers up to n that are relatively prime to n
    # 
    # For example pi_set(8) returns U(8) = { 1, 3, 5, 7}
    return [x for x in range(1,n+1,1) if math.gcd(x,n) == 1]