import numpy as np

from sspinn.nn_translator import nn_translator as nnt


def assert_raises(func, error, *args, **kwargs):
    """ Tests if a function throws the specified exception """
    try:
        func(*args, **kwargs)
    except error:
        return True
    else:
        assert False, 'Bad handling of {0} in {1}'.format(error, func)


def test_nn_translator():
    """ Test sspinn.nn_translator """

    non_str = 0
    non_bool = 0
    fake_file = 'i_dont_exist.fake'
    bad_file = 'data/nn_translator_bad.csv'
    good_file = 'data/nn_translator_data.csv'

    # Check defensive programming
    assert_raises(nnt, TypeError, non_str)
    assert_raises(nnt, TypeError, good_file, train=non_bool)
    assert_raises(nnt, FileNotFoundError, fake_file)
    assert_raises(nnt, ValueError, bad_file)

    # Form expected vector
    emp_frm = np.zeros((10,))
    emp_frm[0] = 22
    emp_frm[1] = 15
    emp_frm[3] = 2
    bounds = (0, 333.8)
    npts = int((bounds[1]-bounds[0])*10)
    peak_dict = {'9.1': 'Q',
                 '10.9': 'Q',
                 '24.2': 'Q',
                 '26.6': 'Q',
                 '27.4': 'T',
                 '33.0': 'T',
                 '39.0': 'T',
                 '44.1': 'S',
                 '46.2': 'D',
                 '72.7':  'D',
                 '121.6': 'D',
                 '125.6': 'S',
                 '138.1': 'S',
                 '165.9': 'S',
                 '200.1': 'S'}
    peak_vec = np.zeros((npts,))
    for peak, mult in peak_dict.items():
        print((peak, mult))
        loc = int((peak-bounds[0])*10)
        if mult == 'S':
            m = 1
        elif mult == 'D':
            m = 2
        elif mult == 'T':
            m = 3
        elif mult == 'Q':
            m = 4
        peak_vec[loc] = m
    expected_vec = np.concat([emp_frm, peak_vec])

    # Get expected connectivity
    expected_conn = np.loadtxt('data/nn_translator_conn.txt')

    # Check treating training like testing data
    result = nnt(good_file)
    assert isinstance(result[0], list)
    assert result[1] is None
    assert len(result[0]) == expected_vec.shape[0]
    assert all(result[0] == expected_vec)

    # Check testing data
    result = nnt('data/nn_translator_test.csv')
    assert isinstance(result[0], list)
    assert result[1] is None
    assert len(result[0]) == expected_vec.shape[0]
    assert all(result[0] == expected_vec)

    # Check training data
    result = nnt(good_file, train=True)
    assert isinstance(result[0], list)
    assert isinstance(result[1], list)
    assert len(result[0]) == expected_vec.shape[0]
    assert all(result[0] == expected_vec)
    assert len(result[1]) == expected_conn.shape[0]
    assert all(result[1] == expected_conn)
