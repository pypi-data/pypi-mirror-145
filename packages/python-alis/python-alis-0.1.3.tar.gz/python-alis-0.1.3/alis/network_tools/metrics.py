"""Metrics when describing a network"""

import networkx as nx


def average_degree(G):
    """Calculates the average degree of a graph 

    Parameters
    ----------
    G : networkx graph

    Returns
    -------
    float
    average degree of a graph  
    """
    degree = G.degree()

    degree_list = []

    for (_, d) in degree:
        degree_list.append(d)

    av_degree = sum(degree_list) / len(degree_list)

    return av_degree


def betweenness_centrality(G):
    """Calculates the betweenness centrality of each node in a graph 

    Parameters
    ----------
    G : networkx graph

    Returns
    -------
    sorted list of degree centrality values of each node 
    """

    print("Betweenness centrality:")
    for k, v in sorted(nx.betweenness_centrality(G).items(), key=lambda x: -x[1]):
        print(str(k)+":"+"{:.3}".format(v)+" ", end="")
    print("\n")


def closeness_centrality(G):
    """Calculates the closeness centrality of each node in a graph 

    Parameters
    ----------
    G : networkx graph

    Returns
    -------
    sorted list of degree centrality values of each node 
    """

    print("Closeness centrality:")
    for k, v in sorted(nx.closeness_centrality(G).items(), key=lambda x: -x[1]):
        print(str(k)+":"+"{:.3}".format(v)+" ", end="")
    print("\n")


def degree_centrality(G):
    """Calculates the degree centrality of each node in a graph 

    Parameters
    ----------
    G : networkx graph

    Returns
    -------
    sorted list of degree centrality values of each node 
    """
    print("Degree centrality:")
    for k, v in sorted(nx.degree_centrality(G).items(), key=lambda x: -x[1]):
        print(str(k)+":"+"{:.3}".format(v)+" ", end="")
    print("\n")


def eigenvector_centrality(G):
    """Calculates the eigenvector centrality of each node in a graph 

    Parameters
    ----------
    G : networkx graph

    Returns
    -------
    sorted list of degree centrality values of each node 
    """

    print("Eigenvector centrality:")
    for k, v in sorted(nx.eigenvector_centrality(G).items(), key=lambda x: -x[1]):
        print(str(k)+":"+"{:.3}".format(v)+" ", end="")
    print("\n")
