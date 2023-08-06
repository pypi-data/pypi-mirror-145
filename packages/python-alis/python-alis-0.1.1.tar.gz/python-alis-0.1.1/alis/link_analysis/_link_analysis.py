"""
Functions helpful for link analysis of datasets.
"""


import numpy as np
import networkx as nx


def idealized_page_rank(M, tol=10**-6, max_iter=100):
    """
    Compute the Idealized PageRank (without Taxation) of a given Transition Matrix    

    Parameters
    ----------
    M : numpy array
        Transition Matrix: Array of shape (n, n), where n is the number of nodes in the network
    tol : float
        Tolerance: Iteration stops if the distance between previous and updated PageRank vectors 
        goes below this value
    max_iter : integer
        Maximum number of iterations

    Returns
    -------
    v : numpy array
        Vector of size n containing the ordinary PageRank values 
    """
    n = M.shape[0]
    v = np.ones(n)/n
    delta = 1/tol  # initialize vector difference to a large number
    i = 0
    while delta > tol:
        i += 1
        prev_v = v
        v = M.dot(v)
        delta = np.sum(np.abs(v-prev_v))
        if i >= max_iter:
            break
    return v


def transition_matrix(G):
    """
    Compute the Transition Matrix given a NetworkX graph

    Parameters
    ----------
    G : NetworkX graph
        Graph to extract the transition matrix

    Returns
    -------
    M : numpy array
        Numpy array of the transition matrix of G
    """
    A = nx.adjacency_matrix(G).toarray()
    d = np.array([x[1] for x in list(G.out_degree)])

    # get indices with zero and replace them with 1 to avoid division by zero
    # this won't affect the result since the corresponding column will have all zeros
    d[d == 0] = 1

    M = A.T * (1/d)
    return M


def taxed_page_rank(M, beta=0.8, tol=10**-6, max_iter=100):
    """Compute the Taxed PageRank (without Taxation) of a given Transition Matrix    
       Note that this not make use of `e` -- the vector of ones 
       since numpy's broadcasting takes care of properly computing a vector-constant addition

    Parameters
    ----------
    M : numpy array
        Transition Matrix: Array of shape (n, n), where n is the number of nodes in the network
    tol : float
        Tolerance: Iteration stops if the distance between previous and updated PageRank vectors 
        goes below this value
    max_iter : integer
        Maximum number of iterations

    Returns
    -------
    v : numpy array
        Vector of size n containing the ordinary PageRank values 
    """
    n = M.shape[0]
    v = np.ones(n)
    delta = 1/tol  # initialize vector difference to a large number
    i = 0
    while delta > tol:
        i += 1
        prev_v = v
        v = beta*M.dot(v) + ((1-beta)/n)
        delta = np.sum(np.abs(v-prev_v))  # compute L1 norm
        if i >= max_iter:
            break
    return v


def topic_sensitive_page_rank(M, S, beta=0.8, tol=10**-6, max_iter=100):
    """Compute the topic-sensitive PageRank (with taxation) of a given Transition Matrix 

    Parameters
    ----------
    M : numpy array
        Transition Matrix: Array of shape (n, n), where n is the number of nodes in the network
    beta :  float
        probability of following an outlink
    S :  list
        indices of pages belonging to the teleport set (indices start at 0)
    tol : float
        Tolerance: Iteration stops if the distance between previous and updated PageRank vectors 
        goes below this value
    max_iter : integer
        Maximum number of iterations

    Returns
    -------
    v : numpy array
        Vector of size n containing the PageRank values 
    """

    n = M.shape[0]
    e = np.zeros(n)
    for i in S:
        e[i] = 1

    v = np.ones(n)
    delta = 1/tol  # initialize to a large number
    i = 0
    while delta > tol:
        i += 1
        prev_v = v
        v = beta*M.dot(v) + ((1-beta)/len(S))*e
        delta = np.mean(np.abs(v-prev_v))
        if i >= max_iter:
            break
    return v


def spam_mass(M, S, beta=0.8, tol=10**-6, max_iter=100):
    """Compute the spam mass given a set of trustworthy pages

    Parameters
    ----------
    M : numpy array
        Transition Matrix: Array of shape (n, n), where n is the number of nodes in the network
    beta :  float
        probability of following an outlink; passed to page_rank_ts
    S :  list
        indices of trustworthy pages (indices start at 0)
    tol : float
        Tolerance: Iteration stops if the distance between previous and updated PageRank vectors 
        goes below this value
    max_iter : integer
        Maximum number of iterations

    Returns
    -------
    p : numpy array
        Vector containing the spam mass 
    """
    r = idealized_page_rank(M, tol=tol, max_iter=max_iter)
    t = topic_sensitive_page_rank(
        M, S=S, beta=beta, tol=tol, max_iter=max_iter)
    p = (r-t)/r
    return p


def hits(L, tol=10**-6, max_iter=100):
    """Compute the PageRank of a given Transition Matrix

    Parameters
    ----------
    L : numpy array
        Link Matrix: Array of shape (n, n), where n is the number of nodes in the network
    tol : float
        Tolerance: Iteration stops if the distance between previous and updated PageRank vectors 
        goes below this value
    max_iter : integer
        Maximum number of iterations

    Returns
    -------
    h, a : tuple of numpy array
        Vectors of size n containing the hub and authority values 
    """
    h = np.ones(L.shape[0])
    a = np.ones(L.shape[0])
    delta = 1/tol  # initialize to a large number
    i = 0
    while delta > tol:
        i += 1

        # save old values
        prev_h = h
        prev_a = a

        # update a
        a = L.T.dot(h)
        # scale a
        a = a/np.max(a)

        # update h
        h = L.dot(a)
        # scale h
        h = h/np.max(h)

        delta = np.mean([
            np.sum(np.abs(h-prev_h)),
            np.sum(np.abs(a-prev_a))
        ])
        if i >= max_iter:
            break
    return h, a
