"""Plotter functions for network analysis"""

from collections import defaultdict

import numpy as np
import networkx as nx
from matplotlib import cm
from matplotlib import colors
import matplotlib.pyplot as plt


def draw_communities(G, membership, pos):
    """Draws the nodes to a plot with assigned colors for each individual cluster

    Parameters
    ----------
    G : networkx graph
    membership : list
        A list where the position is the student and the value at the position is the student club membership.
        E.g. `print(membership[8]) --> 1` means that student #8 is a member of club 1.
    pos : positioning as a networkx spring layout
        E.g. nx.spring_layout(G)

    Returns
    -------
    Network with assigned colors for each community 
    """

    fig, ax = plt.subplots(figsize=(16, 9))

    # Convert membership list to a dict where key=club, value=list of students in club
    club_dict = defaultdict(list)
    for student, club in enumerate(membership):
        club_dict[club].append(student)

    # Normalize number of clubs for choosing a color
    norm = colors.Normalize(vmin=0, vmax=len(club_dict.keys()))

    for club, members in club_dict.items():
        nx.draw_networkx_nodes(G, pos,
                               nodelist=members,
                               node_color=cm.jet(norm(club)),
                               node_size=500,
                               alpha=0.8,
                               ax=ax)

    # Draw edges (social connections) and show final plot

    nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax)


def graph_to_edge_matrix(G):
    """Convert a networkx graph into an edge matrix.

    Parameters
    ----------
    G : networkx graph

    Returns
    -------
    array: edge matrix     
    """

    # Initialize edge matrix with zeros
    edge_mat = np.zeros((len(G), len(G)), dtype=int)

    # Loop to set 0 or 1 (diagonal elements are set to 1)
    for node in G:
        for neighbor in G.neighbors(node):
            edge_mat[node][neighbor] = 1
        edge_mat[node][node] = 0

    return edge_mat


def plot_degree_distribution(G):
    """Plots the degree distribution of a graph 

    Parameters
    ----------
    G : networkx graph

    Returns
    -------
    degree distribution plot 
    """

    degree = G.degree()

    degree_list = []

    for (_, d) in degree:
        degree_list.append(d)

    av_degree = sum(degree_list) / len(degree_list)

    plt.hist(degree_list, label='Degree Distribution')
    plt.axvline(av_degree, color='r', linestyle='dashed',
                label='Average Degree')
    plt.legend()
    plt.ylabel('Number of Nodes')
