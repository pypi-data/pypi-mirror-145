"""
Class definition for Minhash signature extraction 
"""

from ..shingles import hashed_word_shingles
from .hash_functions import create_hash_functions


def get_signature(nonzero_rows, num_hash, hash_size=None, seed=1337):
    """Return the hash signature of the given document with the nonzero
    row indices specified by `nonzero_rows`.

    Other parameters are those that are required by the creation of the
    hash functions needed to generate the signature.

    Parameters
    ----------
    nonzero_rows : iterable of int
        Iterable containing the indices of rows with non-zero values
    num_hash : int
        Number of hash fucntions to generate
    hash_size : int, default=None
        Range of the hash function D. If not specified, this defaults
        to 2**32
    seed : int, default=1337
        Random seed to use during random number generation

    Returns
    -------
    signature : list of int
        List containing the minhash signature of the document
    """
    hash_functions = create_hash_functions(num_hash, hash_size, seed)

    return [min(hash_function(x) for x in nonzero_rows)
            for hash_function in hash_functions]


class MinhashLSH:
    """
    Base class definition for extraction of the minhash signature given
    a dask bag of text data.

    Attributes
    ----------
    shingle_size : int
        Shingle size to use for hashed word shingle extraction
    num_shingle_bucket : int
        The number defining the bucket size for word shingles. This
        is equal to 2**n - 1
    num_hash : int
        Number of randomized hash functions to use in minhash
        signature extraction.
    hash_size : int, default=None
        Range of hte hash function. If not specified, this defaults
        to 2**32
    seed : int, default=1337
        Random seed to use during random number generation
    """

    def __init__(self, shingle_size, num_shingle_bucket, num_hash,
                 hash_size=None, stop_words=None, seed=1337):
        """Initialize the Minhash LSH signature extractor

        Parameters
        ----------
        shingle_size : int
            Shingle size to use for hashed word shingle extraction
        num_shingle_bucket : int
            The number defining the bucket size for word shingles. This
            is equal to 2**n - 1
        num_hash : int
            Number of randomized hash functions to use in minhash
            signature extraction.
        hash_size : int, default=None
            Range of hte hash function. If not specified, this defaults
            to 2**32
        stop_words : iterable of str, default=None
            List of stop words to be used. By default, uses the English
            stopwords defined by sklearn
        seed : int, default=1337
            Random seed to use during random number generation
        """
        self.shingle_size = shingle_size
        self.num_shingle_bucket = num_shingle_bucket
        self.num_hash = num_hash
        self.hash_size = hash_size
        self.stop_words = stop_words
        self.seed = seed

    def transform(self, db_text):
        """Return a dask bag containing the minhash signatures of
        documents in the given dask bag of text

        Parameters
        ----------
        db_text : dask.bag object
            Dask bag object containing texts and their document
            identifier. Each element in the dask bag will be a tuple
            with the first element being the identifier and the
            second element being the text.

            This allows us to perform mapping function via:
            
            ```
            db_text.map(lambda x: (x[0], map_function(x[1], **kwargs)))
            ```

        Returns
        -------
        db_minhash : dask.bag object
            Dask bag object containing the minhash signature of each
            document along with its identifier.
        """
        word_shingles = db_text.map(lambda x: (
            x[0],
            hashed_word_shingles(
                x[1], self.shingle_size,
                self.num_shingle_bucket, self.stop_words)
            )
        ).filter(lambda x: len(x[1]) > 0)
        db_minhash = word_shingles.map(lambda x: (
            x[0],
            get_signature(x[1], self.num_hash, self.hash_size, self.seed)
            )
        )
        return db_minhash
