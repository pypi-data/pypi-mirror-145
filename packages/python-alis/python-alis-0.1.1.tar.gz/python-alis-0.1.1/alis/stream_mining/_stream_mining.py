"""Helper functions for processing streams"""

import numpy as np
import hashlib
import random

def alonMatiasSzegedy(iterator, k_moment=2, num_variables=3, var_prob=0.1):
    """
    Compute the Kth order moment of a stream using Alon-Matias-Szegedy algorithm

    Parameters
    ----------
    iterator : iterator
        Iterator of data of any type
    k_moment : int
        Kth order of moment to calculate for
    num_variables : integer
        Number of variables to keep for the AMS algorithm
    var_prob : float
        Probability for next data value to be treated as a variable

    Returns
    -------
    moment : int
        Kth order moment of a stream
    """
    
    variables = {}
    n = 0
  
    for val in iterator:
        n += 1
        
        if val not in variables:
            if len(variables) < num_variables and random.random() < var_prob:
                variables[val] = 1
        else:
            variables[val] += 1


    amsMoment = 0
    for w in variables:
        amsMoment +=   n * (variables[w]**k_moment - ((variables[w] - 1)**k_moment))

    amsMoment /= len(variables)
    return amsMoment


def flajoletMartin(iterator):
    """
    Count the number of distinct elements in a stream using the Flajolet-Martin algorithm

    Parameters
    ----------
    iterator : iterator
        Iterator of data of any type

    Returns
    -------
    count : int
        Approximation of the number of distinct elements
    """
    
    max_tail_length = 0
    
    for val in iterator:
        bit_string = bin(hash(hashlib.md5(val.encode('utf-8')).hexdigest()))
        
        i = len(bit_string) - 1
        tail_length = 0
        while i >= 0:
            if bit_string[i] == '0':
                tail_length += 1
            else:
                #neatly handles the '0b' prefix of the binary string too. 
                #Just break when we see "b"
                break
                
            i -= 1
            
        if tail_length > max_tail_length:
            max_tail_length = tail_length
            
    return (2**max_tail_length)
