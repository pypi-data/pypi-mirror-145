"""Scalable network clustering tools"""


import networkx as nx
import operator


def weight(c):
    return float(2 * nx.number_of_edges(c) / nx.number_of_nodes(c))


def orderVertex(g):
    d = nx.pagerank(g)
    sorted_v = list(map(lambda x: x[0], sorted(
        d.items(), key=operator.itemgetter(1), reverse=True)))
    return sorted_v


def LA(G):
    """Link Aggregate algorithm implementation

    Taken from: https://github.com/justin830827/Overlapping-Community-Detection/blob/master/LA.py
    """
    clusters = []
    vertex = orderVertex(G)
    # Iterate through each vertex
    for v in vertex:
        add = False
        # Iterate through all existing cluster to search if current vertex belongs to one of them
        for j in range(len(clusters)):
            U = clusters[j] + [v]
            UW = float(2 * nx.number_of_edges(G.subgraph(U)) /
                       nx.number_of_nodes(G.subgraph(U)))
            W = float(
                2 * nx.number_of_edges(G.subgraph(clusters[j])) / nx.number_of_nodes(G.subgraph(clusters[j])))
            if UW > W:
                clusters[j] += [v]
                add = True

        # If the vertex doesn't belong to one of the existing cluster, create a new cluster
        if add == False:
            clusters.append([v])

    # Return a list of cluster
    return clusters


def IS2(cluster, G):
    """Iterative Scan (IS2) algorithm implementation

    Taken from https://github.com/justin830827/Overlapping-Community-Detection/blob/master/IS2.py
    """
    # Build a subgraph using input cluster
    cur = G.subgraph(cluster)
    # Calculate the current communication density
    W = float(2*nx.number_of_edges(cur)/nx.number_of_nodes(cur))
    increase = True
    # Continue iterate if there are any improvement of communication density
    while increase:
        N = list(cur.nodes)
        # Use cluster as candidate set and find adjacent vertices. Append adjacent vertices to candidate set.
        for vertex in cur.nodes:
            adj = G.neighbors(vertex)
            N = list(set(N).union(set(adj)))
        # Iterate all vertex in candidate set to see if it improves communication density.
        for vertex in N:
            original_vertex = list(cur.nodes)
            if vertex in original_vertex:
                original_vertex.remove(vertex)
            else:
                original_vertex.append(vertex)
            if not original_vertex:
                new_cur_w = 0
            else:
                new_cur = G.subgraph(original_vertex)
                new_cur_w = float(
                    2 * nx.number_of_edges(new_cur) / nx.number_of_nodes(new_cur))
            cur_w = float(2 * nx.number_of_edges(cur) /
                          nx.number_of_nodes(cur))
            if new_cur_w > cur_w:
                cur = new_cur.copy()
        new_W = float(2 * nx.number_of_edges(cur) / nx.number_of_nodes(cur))
        # If the new communication density do not increase, then it is converge.
        if new_W == W:
            increase = False
        else:
            W = new_W

    # Return new cluster
    return list(cur.nodes)
