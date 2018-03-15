import keras
from sspinn.predict import Predictor


try:
    NotADirectoryError
except NameError:
    NotADirectoryError = OSError


def test__init__():
    """Test for proper initialization of keras model"""

    # Tests that a filled keras model is loaded for prediction
    test_predictor = Predictor(train=True, test=True)
    assert isinstance(test_predictor._nn, keras.models.Sequential), \
        "_nn is not Keras model"
    assert len(test_predictor._nn.layers) != 0, \
        "Keral model did not fill layers"

    # Tests that a filled keras model is loaded for testing
    test_predictor = Predictor(train=False, test=True)
    if test_predictor._data is None:
        pass
    else:
        raise Exception('_data is not empty when testing')
    if test_predictor.load_nn() is None:
        pass
    else:
        raise Exception('Does not initiate empty string for writing \
            trained net')


def test_set_nn():
    """Testing the safe method of setting custom nets"""

    # Tests that setting new net is checked by ._check_net
    test_predictor = Predictor(train=False, test=True)
    nn = 'nn_string.h5'
    try:
        test_predictor.set_nn(nn)
    except TypeError:
        pass
    else:
        print('TypeError not handled for loading custom net')


def test_load_nn():
    """Tests that correct error is thrown if  incorrect nn is loaded"""

    # Passing the function a list
    net = ['not', 'a', 'string']
    try:
        Predictor(net, test=True)
    except TypeError:
        pass
    else:
        print('TypeError not handled for input net data type')


def test_load_data():
    """Tests for handling of default data directories"""

    # Passing the function a string
    data_dir = 'not_directory'
    try:
        Predictor(data_dir, test=True)
    except NotADirectoryError:
        pass
    else:
        print('NotADirectoryError not handled for input data set')


def test_check_net():
    """Test that correct error is thrown in case of passing incorrect nn"""

    # Passing the function a string
    nn = 'not_keras_model'
    try:
        Predictor(nn, test=True)
    except TypeError:
        pass
    else:
        print('TypeError not handled for predictor._nn')
