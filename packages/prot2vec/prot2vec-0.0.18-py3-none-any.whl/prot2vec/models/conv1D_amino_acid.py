from tensorflow.keras.layers import Conv1D, BatchNormalization, Dropout, Input, Activation, Conv1DTranspose
from tensorflow.keras.models import Model

from prot2vec.layers.skip_block_conv1d import conv1D_conv_block, conv1D_deconv_block, conv1D_identity_block


def conv1d_model(seq_len, onehot_size, dropout=0.1):
    x_input = Input((seq_len, onehot_size))

    x = Conv1D(128, kernel_size=9, strides=2, padding='same')(x_input)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Dropout(dropout)(x)

    # Define size of sub-blocks and initial filter size
    block_layers = [2, 3, 3, 2]
    kernels = 128
    # Step 3 Add the Resnet Blocks
    for i in range(4):
        if i == 0:
            # For sub-block 1 Residual/Convolutional block not needed
            for j in range(block_layers[i]):
                x = conv1D_identity_block(x, kernels, 5)
        else:
            # One Residual/Convolutional Block followed by Identity blocks
            # The filter size will go on increasing by a factor of 2
            kernels = kernels * 2
            x = conv1D_conv_block(x, kernels, 5)
            for j in range(block_layers[i] - 1):
                x = conv1D_identity_block(x, kernels, 5)

    #############
    # Define size of sub-blocks and initial filter size
    block_layers = [2, 3, 3]
    kernels = 1024
    # Step 3 Add the Resnet Blocks
    for i in range(3):
        kernels = kernels / 2
        x = conv1D_deconv_block(x, kernels, 5)
        for j in range(block_layers[i] - 1):
            x = conv1D_identity_block(x, kernels, 5)

    x = Conv1DTranspose(onehot_size, 9, padding='same', strides=2)(x)
    ae_out = Activation('softmax', name='ae_out')(x)

    model = Model(inputs=x_input, outputs=ae_out, name="conv1d_model")

    return model
