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
