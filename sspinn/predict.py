import os
import pickle
import keras
import numpy as np


_N_DIMS_IN = 3350
_N_DIMS_OUT = 186624

# Python 2 compatibility
try:
    NotADirectoryError
except NameError:
    NotADirectoryError = IOError


class Net(keras.models.Sequential):
    """Wrapper around a keras Sequential net that has a default architecture"""

    def __init__(self):
        keras.models.Sequential.__init__(self)
        self._arch()
        self.compile(optimizer='sgd', loss='mean_squared_error')

    def _arch(self):
        self.add(keras.layers.Dense(1000, input_dim=_N_DIMS_IN))
        self.add(keras.layers.Activation('elu'))
        self.add(keras.layers.Dropout(0.5))
        self.add(keras.layers.Dense(3000))
        self.add(keras.layers.Activation('sigmoid'))
        self.add(keras.layers.Dropout(0.3))
        self.add(keras.layers.Dense(_N_DIMS_OUT))
        self.add(keras.layers.Activation('relu'))


class Predictor(object):
    """Contains NN and helper functions"""

    def __init__(self, train=False, data_dir='../data', net='last_trained.h5'):
        if train:
            self._data = np.empty((0, _N_DIMS_IN))
            self._target = np.empty((0, _N_DIMS_OUT))
            self._load_data(data_dir)
            self._nn = Net()
        else:
            self._data = None
            self.load_nn(net=net)
        self.history = None

    def set_nn(self, nn):
        """ Safe method for setting custom net """
        self._check_net(nn)
        self._nn = nn

    def train(self, filepath='sspinn/nets/last_trained.h5', epochs=10000,
              validation_split=0.2, **kwargs):
        """ Main method for training the neural net """
        chkpt = keras.callbacks.ModelCheckpoint(filepath, save_best_only=True)
        bar = keras.callbacks.ProgbarLogger(count_mode='samples')
        self._check_net(self._nn)
        hist = self._nn.fit(x=self._data, y=self._target,
                            epochs=epochs, callbacks=[chkpt, bar],
                            validation_split=validation_split,
                            **kwargs)
        self.history = hist.history
        with open('nets/last_history.pkl', 'wb') as fil:
            pickle.dump(self.history, fil)

    def load_nn(self, net='last_trained.h5'):
        """ Loads a previously trained neural net for prediction """

        nets_dir = __file__.strip('predict.py')
        nets_dir += 'nets'
        print(nets_dir)
        if not isinstance(net, str):
            raise TypeError('Input "net" is not string')

        if not os.path.isdir(nets_dir):
            raise NotADirectoryError('Directory nets/ does not exist')
        if net in os.listdir(nets_dir):
            self._nn = Net()
            self._nn.load_weights(nets_dir + '/' + net)

    def _load_data(self, data_dir):
        """ Loading default data """
        if not os.path.isdir(data_dir):
            raise NotADirectoryError(
                'Directory {0} does not exist'.format(data_dir)
            )
        print('Loading data...')
        self._data = np.load(data_dir + '/preprocessed_input.npy')
        print('Loading target...')
        self._target = np.load(data_dir + '/preprocessed_target.npy')

    def _check_net(self, nn):
        """ Error checking for the net """
        if not isinstance(nn, keras.models.Model):
            raise TypeError("Passed net is not a keras model")
        # We ignore compilation. The user needs to do it manually if not
        # through the Net object
