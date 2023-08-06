"""
The traditional LSH appraoch to a hypothetical many-to-many document similarity task. 
The objective is to bucket similar documents together. The implementation is done through 
the `LSH` class which leverages on `dask.bag` functionality and methods to 
parallelize the banding technique. Specifically, the map (hash function) and reduce 
(bucketing) tasks.

Note: importing the model automatically initializes a dask client.

BY: Mike Dorosan, 2022
"""

import dask.bag as db

import numpy as np
import matplotlib.pyplot as plt


class LSH():
    """The LSH class for a many-to-many document similarity task.

    Attributes
    ----------
    signature : 2-D np.array
        document minhash signatures with dimension n (samples) by m (signature size)
    bands : int
        number of bands
    r : int
        number of rows per band derived from bands
    hash_functions : list, default=None
        a list of hash functions with size equivalent to the number of 
        bands. If None, the native python hash function is applied.
    band_dict : dict
        dictionary with band labels as keys and 
        (set/doc index, signature band) tuples as values  
    band_buckets : dict
        a dictionary with hash bucket as keys and a list of similar 
        document indices as values
    Methods
    -------

    """

    def __init__(self, signature):
        """Initialize class

        Parameters
        ----------
        signature : 2-D np.array, or dask.bag 
            document minhash signatures with dimension n (samples) by m (signature size)
            dask.bag of tuples (set/doc index, )
        """
        self.signature = signature
        self.bands = None  # number of bands
        self.r = None  # rows per band, band size
        self.hash_functions = None
        self.band_dict = {}
        self.band_buckets = {}

    def make_bands(self, bands):
        """Takes in the desired number of `bands` as a parameter and returns 
        a dictionary with band labels as keys and `dask.bag` of (set/document 
        index, signature band) tuples

        Parameters
        ----------
        bands : int 
            desired number of bands

        Returns
        -------
        band_dict : dict 
            dictionary with band labels as keys and 
            (set/doc index, signature band) tuples as values    
        """

        self.bands = bands
        
        if type(self.signature) == db.core.Bag:
            signature_size = len(self.signature.take(1)[0][1]) # get size of signature
            assert signature_size % self.bands == 0, "Number of bands not a factor of signature size."
            self.r = int(signature_size / self.bands)
            
            for band_label, i in enumerate(range(0, signature_size, self.r)):
                band_bag = self.signature.map(lambda x: (x[0], np.array(x[1][i:i+self.r]))).repartition(1)
                self.band_dict[band_label] = band_bag
            
        elif type(self.signature) == np.ndarray:
            # check if number of bands divide columns equally
            signature_size = self.signature.shape[1]
            assert signature_size % self.bands == 0, "Number of bands not a factor of signature size."

            self.r = int(signature_size / self.bands)

            for band_label, i in enumerate(range(0, signature_size, self.r)):
                band_bag = db.from_sequence(
                    zip(range(signature_size),
                        self.signature[:, i:i+self.r]), npartitions=1)
                self.band_dict[band_label] = band_bag
                
        else:
            raise "Input signature not a dask.bag.core.Bag or a numpy.ndarry"


        return self.band_dict

    def get_buckets(self, hash_functions=None, compute=False):
        """This method implementes the map-reduce step of the traditional 
        banding technique. Specifically, signature slices of each band are 
        hashed using `hash_functions` (map). The document indices are then 
        grouped according to their hash values.

        Parameters
        ----------
        hash_functions : list, default=None
            a list of hash functions with size equivalent to the number of 
            bands. If None, the native python hash function is applied.

        Returns
        -------
        band_buckets - dict 
            a dictionary with hash bucket as keys and a list of similar 
            document indices as values    
        """

        self.hash_functions = hash_functions
        if not hash_functions:
            # use python's built-in hasher
            self.hash_functions = [hash]

        for index, (key, value) in enumerate(self.band_dict.items()):
            # add checks here for hash_functions type
            if len(self.hash_functions) > 1:
                idx = index
            else:
                idx = 0
            self.band_buckets[key] = (
                value.map(
                    lambda x: (
                        x[0],
                        self.hash_functions[idx](x[1].tobytes())
                    )
                )
                .groupby(lambda x: x[1])  # groupby hash value
                # get only document index
                .map(lambda x: (x[0], list(list(zip(*x[1]))[0])))
            )
            if compute:
                self.band_buckets[key] = self.band_buckets[key].compute()

        return self.band_buckets

    def _prob_of_s(self, s):
        """Return the probability of similarity s given b and r"""
        return 1 - (1 - s**self.r)**self.bands

    def _get_approx_thresh(self):
        """Return approximate similarity threshold for chosen b and r"""
        thresh = (1/self.bands) ** (1/self.r)

        return thresh

    def plot_thresh(self, return_thresh=True, display_thresh=True, ax=None, **kwargs):
        """Plots the threshold plot according to number of bands.

        Parameters
        ----------
        display_thresh : bool, default=True 
            whether to display emphasis on the similarity threshold or not.

        ax : matplotlib.pyplot Axis, default=None 
            Axis for plotting. If None, use internally generated Axis object.

        **kwargs : keyword arguments for the matplotlib.pyplot.plot() function.

        Returns
        -------
        ax : matplotlib.pyplot Axis object
        """
        s_list = np.linspace(0, 1, num=50)
        p_list = np.array([self._prob_of_s(s) for s in s_list])

        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))

        ax.plot(s_list, p_list, **kwargs)
        thresh = self._get_approx_thresh()
        if display_thresh:
            ax.axvline(thresh, color='black', linestyle='--',
                       label=f'Similarity Threshold: {thresh:.2f}')

        ax.set_title('Probability of becoming a candidate given a similarity\nThe S-curve',
                     fontsize=15)
        ax.set_ylabel('Probability', fontsize=13)
        ax.set_xlabel('Jaccard Similarity of Documents', fontsize=13)
        
        # Hide the right and top spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # set spines lw
        ax.spines['left'].set_linewidth(3)
        ax.spines['bottom'].set_linewidth(3)
        
        ax.legend(fontsize=13)
        self.ax_ = ax
        if return_thresh:
            return self.ax_, thresh
        return self.ax_
    
