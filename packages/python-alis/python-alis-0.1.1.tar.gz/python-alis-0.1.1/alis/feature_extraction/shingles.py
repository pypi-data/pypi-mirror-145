"""
Functions for extracting different types of
shingles given a text.
"""

import hashlib

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


def hash_function(text, n):
    """Return the integer hash function representation given text and
    the number of buckets n

    Parameters
    ----------
    text : str
        String of text whose hash representation is to be computed
    n : int
        The number definining the bucket size: 2**n - 1

    Returns
    -------
    hashed_int : int
        Hashed representation of the given text
    """
    return int(hashlib.sha1(text.encode('utf-8')).hexdigest(), 16) % (2**n - 1)


def k_shingles(text, k):
    """Return all the k-shingles of the text

    Parameters
    ----------
    text : str
        String of text in which shingles are to be extracted
    k : int
        Shingle size

    Returns
    -------
    shingles : iterable
        An iterable of all k-shingles in the input text
    """
    return set([text[i:i+k] for i in range(0, len(text) - k + 1)])


def hashed_shingles(text, k, n):
    """Return all the `k`-shingles in the given `text` hashed into a
    bucket number in the range 0 to 2**`n` - 1

    Parameters
    ----------
    text : str
        String of text in which shingles are to be extracted
    k : int
        Shingle size
    n : int
        The number defining the bucket size 2**n - 1

    Returns
    -------
    shingles : iterable of int
        An iterable of all k-shingles in the input text hashed into
        buckets
    """
    return set([
        hash_function(text[i:i+k], n)
        for i in range(0, len(text) - k + 1)])


def word_shingles(text, k, stop_words=None):
    """Return the list of word `k`-shingles from the given text based
    on a given stop words.

    We define a shingle to be a stop word followed by the next `k-1`
    words regardless of whether the next words were stop words or not.

    Parameters
    ----------
    text : str
        String of text whose word shingles are to be extracted
    k : int
        Shingle size
    stop_words : iterabe of str, default=None
        List of stop words to be used. By default, uses the English
        stopwords defined by sklearn

    Returns
    -------
    shingles : iterable of str
        A list containing the extracted word shingles in a document.
    """
    # Define stop words if none is given
    if stop_words is None:
        stop_words = ENGLISH_STOP_WORDS
    splitted_text = text.split()

    return set([
        ' '.join(splitted_text[i:i + k])
        for i in range(len(splitted_text) - k + 1)
        if splitted_text[i] in stop_words
    ])


def hashed_word_shingles(text, k, n, stop_words=None):
    """Return the list of word `k`-shingles from the given text based
    on a given stop words then hases it into a bucket with range 0 to
    2**n - 1.

    We define a shingle to be a stop word followed by the next `k-1`
    words regardless of whether the next words were stop words or not.

    Parameters
    ----------
    text : str
        String of text whose word shingles are to be extracted
    k : int
        Shingle size
    n : int
        The number defining the bucket size 2**n - 1
    stop_words : iterabe of str, default=None
        List of stop words to be used. By default, uses the English
        stopwords defined by sklearn

    Returns
    -------
    shingles : iterable of int
        A list containing the extracted word shingles in hashed
        representation.
    """
    # Define stop words if none is given
    if stop_words is None:
        stop_words = ENGLISH_STOP_WORDS
    splitted_text = text.split()

    return set([
        hash_function(' '.join(splitted_text[i:i + k]), n)
        for i in range(len(splitted_text) - k + 1)
        if splitted_text[i] in stop_words
    ])
