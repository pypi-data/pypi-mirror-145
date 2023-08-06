"""
Hash Functions for Minhash Signatures
=====================================

This module contains the hash function definition useful when creating
minhash signatures.
"""

import numpy as np


def create_hash_functions(num_hash, hash_size=None, seed=1337):
    """Return a set of hash functions given the size parameters

    Hash functions generated are basd from the universal hashing
    strategy:

    $$
    hash(x) = (ax + b) mod D
    $$

    where $a, b$ are randomly generated such that $a, b \in [0, D)$

    Parameters
    ----------
    num_hash : int
        Number of hash fucntions to generate
    hash_size : int, default=None
        Range of the hash function D. If not specified, this defaults
        to 2**32
    seed : int, default=1337
        Random seed to use during random number generation

    Returns
    -------
    hash_functions : array of shape (num_hash, num_rows)
        Generated hash functions based on size parameters
    """
    # Set random seed
    np.random.seed(seed)

    # Set hash size if None
    if hash_size is None:
        hash_size = 2**32

    # Generate random values for a and b
    A = np.random.randint(0, hash_size, num_hash)
    B = np.random.randint(0, hash_size, num_hash)

    # Generate hash functions;
    # Note we need to do this to clarify the scope of the lambda function:
    # https://stackoverflow.com/a/34021333
    return [(lambda y, z: (lambda x: (y*x + z) % (hash_size - 1)))(a, b)
            for a, b in zip(A, B)]
