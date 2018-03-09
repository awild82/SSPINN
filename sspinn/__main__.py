import sys
import numpy as np
from . import nn_translator
from . import predict
from . import visualizer

inputfile = sys.argv[1]

nn_input, input_mat, empirical \
      = nn_translator.nn_translator(inputfile, train=True)
nn_input = np.array(nn_input).reshape((1, 3349))

p = predict.Predictor(net='hyak_long.h5')
nn_output = p._nn.predict(nn_input)
nn_output = np.reshape(nn_output, (432, 432))

# Create Visual output
empirical.pop('\n')
real = visualizer.Visualizer(nn_output, empirical)
visual = visualizer.Visualizer(np.array(input_mat), empirical)
visual.draw2Dstructure()
real.draw2Dstructure()
