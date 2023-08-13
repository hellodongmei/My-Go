# tag::alphago_base[]
# from keras.models import Sequential
from tensorflow.keras import Sequential
# from keras.layers.core import Dense, Flatten
# from keras.layers.convolutional import Conv2D
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.layers import Conv2D

# strong policy has 13 layers; value policy has 16 layers

def alphago_fast(input_shape,  # <1>
                  num_filters=192,  # <2>
                  first_kernel_size=5,
                  other_kernel_size=3):  # <3>

    model = Sequential()
    model.add(
        Conv2D(num_filters, first_kernel_size, input_shape=input_shape, padding='same',
               data_format='channels_first', activation='relu'))

    for i in range(2, 4):  # <4>
        model.add(
            Conv2D(num_filters, other_kernel_size, padding='same',
                   data_format='channels_first', activation='relu'))
# <1> With this boolean flag you specify if you want a policy or value network
# <2> All but the last convolutional layers have the same number of filters
# <3> The first layer has kernel size 5, all others only 3.
# <4> The first 12 layers of AlphaGo's policy and value network are identical.
# end::alphago_base[]

# tag::alphago_policy[]
    # if is_policy_net:
    model.add(
        Conv2D(filters=1, kernel_size=1, padding='same',
                data_format='channels_first', activation='softmax'))
    model.add(Flatten())
    return model
# end::alphago_policy[]

# # tag::alphago_value[]
#     else:
#         model.add(
#             Conv2D(num_filters, other_kernel_size, padding='same',
#                    data_format='channels_first', activation='relu'))
#         model.add(
#             Conv2D(filters=1, kernel_size=1, padding='same',
#                    data_format='channels_first', activation='relu'))
#         model.add(Flatten())
#         model.add(Dense(256, activation='relu'))
#         model.add(Dense(1, activation='tanh'))
#         return model
# # end::alphago_value[]
