"""
Module definition of jaccard similarity between two
sets given the characteristic matrix representation.
"""

from scipy.spatial.distance import jaccard


def jaccard_sim(characteristic_matrix, i, j):
    """Return the jaccard similarity of sets i and j given the
    characteristic matrix

    Parameters
    ----------
    characteristic_matrix : arr
        Array of shape (num_items, num_sets) containing the
        characteristic matrix in which the Jaccard similarity is to be
        computed
    i : int
        Index of set i
    j : int
        Index of set j

    Returns
    -------
    sim : float
        Jaccard similarity between the chosen sets i and j
    """
    return 1 - jaccard(characteristic_matrix[:, i],
                       characteristic_matrix[:, j])
