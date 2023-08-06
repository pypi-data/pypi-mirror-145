"""
This module contains functions that will be useful in extracting
features from a given text to be represented as shingles or hashed
functions.
"""

from .minhash import MinhashLSH
from .shingles import (
    k_shingles, hashed_shingles, word_shingles, hashed_word_shingles
)
