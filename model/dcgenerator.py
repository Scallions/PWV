import paddle
import paddle.nn as nn
from .modules.nn import PixelShufflePack
import functools

from paddle.nn import BatchNorm2D
from .modules.norm import build_norm_layer


class DCGenerator(nn.Layer):
    """Resnet-based generator that consists of Resnet blocks between a few downsampling/upsampling operations.
    """
    def __init__(self,
                 input_nz,
                 output_nc,
                 ngf=64,
                 dropout = 0.1,
                 norm_type='batch',
                 padding_type='reflect'):
        """Construct a DCGenerator generator
        Args:
            input_nz (int): the number of channels in input images
            output_nc (int): the number of channels in output images
            ngf (int): the number of filters in the last conv layer
            norm_layer: normalization layer
            padding_type (str): the name of padding layer in conv layers: reflect | replicate | zero
        """
        super(DCGenerator, self).__init__()

        norm_layer = build_norm_layer(norm_type)
        if type(norm_layer) == functools.partial:
            use_bias = norm_layer.func == nn.BatchNorm2D
        else:
            use_bias = norm_layer == nn.BatchNorm2D

        n_downsampling = 5
        mult = 2**(n_downsampling-1)

        if norm_type == 'batch':
            model = [
                nn.Conv2DTranspose(input_nz,
                                   ngf * mult,
                                   kernel_size=4,
                                   stride=1,
                                   padding=0,
                                   bias_attr=use_bias),
                BatchNorm2D(ngf * mult),
                nn.ReLU(),
                nn.Dropout(dropout)
            ]
        else:
            model = [
                nn.Conv2DTranspose(input_nz,
                                   ngf * mult,
                                   kernel_size=4,
                                   stride=1,
                                   padding=0,
                                   bias_attr=use_bias),
                norm_layer(ngf * mult),
                nn.ReLU(),
                nn.Dropout(dropout)
            ]

        # add upsampling layers
        for i in range(1, n_downsampling):
            mult = 2**(n_downsampling - i)
            if norm_type == 'batch':
                model += [
                    # nn.Conv2DTranspose(ngf * mult,
                    #                    ngf * mult // 2,
                    #                    kernel_size=4,
                    #                    stride=2,
                    #                    padding=1,
                    #                    bias_attr=use_bias),
                    PixelShufflePack(ngf * mult,
                                     ngf * mult // 2,
                                     2,
                                     4),
                    BatchNorm2D(ngf * mult // 2),
                    nn.ReLU(),
                    nn.Dropout(dropout)
                ]
            else:
                model += [
                    # nn.Conv2DTranspose(ngf * mult,
                    #                    int(ngf * mult // 2),
                    #                    kernel_size=4,
                    #                    stride=2,
                    #                    padding=1,
                    #                    bias_attr=use_bias),
                    PixelShufflePack(ngf * mult,
                                     ngf * mult // 2,
                                     2,
                                     4),
                    norm_layer(int(ngf * mult // 2)),
                    nn.ReLU(),
                    nn.Dropout(dropout)
                ]

        model += [
            nn.Conv2DTranspose(ngf,
                               output_nc,
                               kernel_size=4,
                               stride=[1,2],
                               padding=1,
                               bias_attr=use_bias),
            # nn.Sigmoid()
            # nn.Tanh()
            # nn.LogSigmoid()
        ]

        self.model = nn.Sequential(*model)

    def forward(self, x):
        b = x.shape[0]
        z = paddle.randn([b, 2000 - 64*24,1,1])
        # t = x.shape[1]
        # d = x.shape[2]
        x = paddle.reshape(x, [b,-1,1,1])
        x = paddle.concat([x,z], axis=1)
        x = self.model(x)
        # return x[:,:,:31,:66].reshape([-1,31,66]) # 调整输出大小
        return x[:,:,:31,:64].reshape([b,24,31,64]) # 调整输出大小
        # return x