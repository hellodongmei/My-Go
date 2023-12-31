from __future__ import absolute_import

# tag::small_network[]
# from keras.layers.core import Dense, Activation, Flatten
from tensorflow.keras.layers import Dense, Activation, Flatten
# from keras.layers.convolutional import Conv2D, ZeroPadding2D
from tensorflow.keras.layers import Conv2D, ZeroPadding2D
from tensorflow.keras import Sequential

def layers(input_shape):
    model = Sequential([
        ZeroPadding2D(padding=3, input_shape=input_shape, data_format='channels_first'),  # <1>
        Conv2D(48, (7, 7), data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D(padding=2, data_format='channels_first'),  # <2>
        Conv2D(32, (5, 5), data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D(padding=2, data_format='channels_first'),
        Conv2D(32, (5, 5), data_format='channels_first'),
        Activation('relu'),

        ZeroPadding2D(padding=2, data_format='channels_first'),
        Conv2D(32, (5, 5), data_format='channels_first'),
        Activation('relu'),

        Flatten(),
        Dense(81),
        Activation('relu'),
    ])
    return model

# <1> We use zero padding layers to enlarge input images.
# <2> By using `channels_first` we specify that the input plane dimension for our features comes first.
# end::small_network[]
