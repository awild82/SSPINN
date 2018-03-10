from sspinn.visualizer import Visualizer
import numpy as np


def test__init__():
    """Test the types of nn ouput data required for visualization package"""

    # Test that np array is required for init
    full = 42
    empirical = {'H': 0, 'C': 0, 'N': 0, 'O': 0}
    try:
        Visualizer(full, empirical)
    except TypeError:
        pass
    else:
        print('TypeError not handled for full array')

    # Test that dictionary is required for init
    full = np.zeros((13, 13))
    empirical = [0, 0, 0]
    try:
        Visualizer(full, empirical)
    except TypeError:
        pass
    else:
        print('TypeError not handled for empirical dictionary')


def test_truncate():
    """Test the function which truncates NN output into a minimal size
    adjacency matrix
    """

    # Test that full matrix can be properly truncated
    full = np.zeros((432, 432))
    empirical = {'H': 1, 'C': 2, 'N': 3, 'O': 4}
    t = Visualizer(full, empirical)
    t._truncate()
    assert t.adjmat.size == 100, "Adjmat is not correct size"

    # Check for correct rows/columns
    full = np.loadtxt('../sspinn/test/sample_nn_output.txt')
    empirical = {'H': 4, 'C': 2}
    expected_trunc = [[0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1],
                      [1, 1, 0, 0, 0, 2], [0, 0, 1, 1, 2, 0]]
    t = Visualizer(full, empirical)
    for i in range(0, t.adjmat.shape[0]):
        assert all(t.adjmat[i] == expected_trunc[i]), \
               "Adjmat did not fill correctly"


def test_genLabels():
    """Test the generation of atomic labels for visualization program"""

    # Test that lists expand from emperical key
    full = np.zeros((432, 432))
    empirical = {'H': 1, 'C': 2, 'N': 3, 'O': 4}
    t = Visualizer(full, empirical)
    t._genLabels()
    assert len(t.labels) == 10, "Atomic label list size incorrect"

    # Test that labels of sorted list are correct
    t.labels.sort()
    assert t.labels == ['C', 'C', 'H', 'N', 'N', 'N', 'O', 'O', 'O', 'O'], \
        "Elements in list incorrect"
