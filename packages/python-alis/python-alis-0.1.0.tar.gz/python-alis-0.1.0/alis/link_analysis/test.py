import unittest
import numpy as np
from numpy.testing import assert_almost_equal
from _link_analysis import *

class IdealizedPageRankTests(unittest.TestCase):

    def test_G1(self):
        M = np.array([
            [  0, 1/2, 1,   0],
            [1/3,   0, 0, 1/2],
            [1/3,   0, 0, 1/2],
            [1/3, 1/2, 0,   0]    
            ])

        pagerank = idealized_page_rank(M)
        self.assertIsInstance(pagerank, np.ndarray)

        assert_almost_equal(
            pagerank, 
            np.array([3/9, 2/9, 2/9, 2/9]),
            decimal=4
        )

    def test_dead_end(self):
        M = np.array([
            [  0, 1/2, 0,   0],
            [1/3,   0, 0, 1/2],
            [1/3,   0, 0, 1/2],
            [1/3, 1/2, 0,   0]    
            ])

        pagerank = idealized_page_rank(M)
        self.assertIsInstance(pagerank, np.ndarray)

        assert_almost_equal(
            pagerank, 
            np.array([0, 0, 0, 0]),
            decimal=4
        )
  
    def test_spider_trap(self):
        M = np.array([
            [  0, 1/2, 0,   0],
            [1/3,   0, 0, 1/2],
            [1/3,   0, 1, 1/2],
            [1/3, 1/2, 0,   0]    
            ])

        pagerank = idealized_page_rank(M)
        self.assertIsInstance(pagerank, np.ndarray)

        assert_almost_equal(
            pagerank, 
            np.array([0, 0, 1, 0]),
            decimal=4
        )
        
class TransitionMatrixTests(unittest.TestCase):
    
    def test_G1(self):
        G1 = nx.DiGraph()
        G1.add_nodes_from(["A","B","C","D"])
        G1.add_edges_from([
            ("A","B"), ("A","C"), ("A","D"), 
            ("B","A"), ("B","D"),
            ("D","B"), ("D","C")
        ])   
        
        M = transition_matrix(G1)
        M_expected = np.array(
            [[0.       , 0.5       , 0.        , 0.        ],
            [0.33333333, 0.        , 0.        , 0.5       ],
            [0.33333333, 0.        , 0.        , 0.5       ],
            [0.33333333, 0.5       , 0.        , 0.        ]])        
        
        self.assertIsInstance(idealized_page_rank(M), np.ndarray)
        assert_almost_equal(M, M_expected, decimal=4)        
        
    def test_G3(self):
        G3 = nx.DiGraph()
        G3.add_nodes_from(["A","B","C","D"])
        G3.add_edges_from([
            ("A","B"), ("A","C"), ("A","D"), 
            ("B","A"), ("B","D"),
            ("C","C"),
            ("D","B"), ("D","C")
        ])
        M = transition_matrix(G3)
        M_expected = np.array([
            [0.        , 0.5       , 0.        , 0.        ],
            [0.33333333, 0.        , 0.        , 0.5       ],
            [0.33333333, 0.        , 1.        , 0.5       ],
            [0.33333333, 0.5       , 0.        , 0.        ]])   
        
        self.assertIsInstance(idealized_page_rank(M), np.ndarray)
        assert_almost_equal(M, M_expected, decimal=4)        

class TaxedPageRankTests(unittest.TestCase):     
    
    def test_G1(self):
        M = np.array([
            [  0, 1/2, 0,   0],
            [1/3,   0, 0, 1/2],
            [1/3,   0, 1, 1/2],
            [1/3, 1/2, 0,   0]    
            ])

        pagerank = taxed_page_rank(M)
        self.assertIsInstance(pagerank, np.ndarray)

        assert_almost_equal(
            pagerank, 
            np.array([15/148, 19/148, 95/148, 19/148]),
            decimal=4
        )        
        
        
class TopicSensitivePageRankTests(unittest.TestCase):     
    
    def test_G1(self):
        M = np.array([
            [  0, 1/2, 1,   0],
            [1/3,   0, 0, 1/2],
            [1/3,   0, 0, 1/2],
            [1/3, 1/2, 0,   0]    
            ])
        
        S = [1,3]
        pagerank = topic_sensitive_page_rank(M, S)
        self.assertIsInstance(pagerank, np.ndarray)

        assert_almost_equal(
            pagerank, 
            np.array([0.25714753, 0.2809555 , 0.1809555 , 0.2809555 ]),
            decimal=4
        )   
        
class SpamMassTests(unittest.TestCase):     
    
    def test_G1(self):
        M = np.array([
            [  0, 1/2, 1,   0],
            [1/3,   0, 0, 1/2],
            [1/3,   0, 0, 1/2],
            [1/3, 1/2, 0,   0]    
            ])
        
        S = [1,3]
        p = spam_mass(M, S)
        self.assertIsInstance(p, np.ndarray)

        assert_almost_equal(
            p, 
            np.array([ 0.22842899, -0.26440674,  0.18558983, -0.26440674]),
            decimal=4
        )           
        
class HitsTests(unittest.TestCase):     
    
    def test_G4(self):
        L = np.array([
            [0, 1, 1, 1, 0],
            [1, 0, 0, 1, 0],
            [0, 0, 0, 0, 1],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0],
            ])
        
        h, a = hits(L)
        self.assertIsInstance(h, np.ndarray)
        self.assertIsInstance(a, np.ndarray)

        assert_almost_equal(
            h, 
            np.array([1, 0.3583, 0, 0.7165, 0]),
            decimal=4
        )
        assert_almost_equal(
            a, 
            np.array([0.2087, 1, 1, 0.7913, 0]),
            decimal=4
        )      
             
        
if __name__ == '__main__':
    unittest.main()
    