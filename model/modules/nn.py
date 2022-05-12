# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserve.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import paddle
import paddle.nn as nn
import math
from .init import kaiming_normal_, constant_


class _SpectralNorm(nn.SpectralNorm):
    def __init__(self,
                 weight_shape,
                 dim=0,
                 power_iters=1,
                 eps=1e-12,
                 dtype='float32'):
        super(_SpectralNorm, self).__init__(weight_shape, dim, power_iters, eps,
                                            dtype)

    def forward(self, weight):
        inputs = {'Weight': weight, 'U': self.weight_u, 'V': self.weight_v}
        out = self._helper.create_variable_for_type_inference(self._dtype)
        _power_iters = self._power_iters if self.training else 0
        self._helper.append_op(type="spectral_norm",
                               inputs=inputs,
                               outputs={
                                   "Out": out,
                               },
                               attrs={
                                   "dim": self._dim,
                                   "power_iters": _power_iters,
                                   "eps": self._eps,
                               })

        return out


class Spectralnorm(paddle.nn.Layer):
    def __init__(self, layer, dim=0, power_iters=1, eps=1e-12, dtype='float32'):
        super(Spectralnorm, self).__init__()
        self.spectral_norm = _SpectralNorm(layer.weight.shape, dim, power_iters,
                                           eps, dtype)
        self.dim = dim
        self.power_iters = power_iters
        self.eps = eps
        self.layer = layer
        weight = layer._parameters['weight']
        del layer._parameters['weight']
        self.weight_orig = self.create_parameter(weight.shape,
                                                 dtype=weight.dtype)
        self.weight_orig.set_value(weight)

    def forward(self, x):
        weight = self.spectral_norm(self.weight_orig)
        self.layer.weight = weight
        out = self.layer(x)
        return out


class RhoClipper(object):
    def __init__(self, min, max):
        self.clip_min = min
        self.clip_max = max
        assert min < max

    def __call__(self, module):

        if hasattr(module, 'rho'):
            w = module.rho
            w = w.clip(self.clip_min, self.clip_max)
            module.rho.set_value(w)

        # used for photo2cartoon training
        if hasattr(module, 'w_gamma'):
            w = module.w_gamma
            w = w.clip(self.clip_min, self.clip_max)
            module.w_gamma.set_value(w)

        if hasattr(module, 'w_beta'):
            w = module.w_beta
            w = w.clip(self.clip_min, self.clip_max)
            module.w_beta.set_value(w)

class PixelShufflePack(nn.Layer):
    """ Pixel Shuffle upsample layer.
    Args:
        in_channels (int): Number of input channels.
        out_channels (int): Number of output channels.
        scale_factor (int): Upsample ratio.
        upsample_kernel (int): Kernel size of Conv layer to expand channels.
    Returns:
        Upsampled feature map.
    """
    def __init__(self, in_channels, out_channels, scale_factor,
                 upsample_kernel):
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.scale_factor = scale_factor
        self.upsample_kernel = upsample_kernel
        self.upsample_conv = nn.Conv2D(self.in_channels,
                                       self.out_channels * scale_factor *
                                       scale_factor,
                                       self.upsample_kernel,
                                       padding=(self.upsample_kernel - 1) // 2)
        self.pixel_shuffle = nn.PixelShuffle(self.scale_factor)
        self.init_weights()

    def init_weights(self):
        """Initialize weights for PixelShufflePack.
        """
        default_init_weights(self, 1)

    def forward(self, x):
        """Forward function for PixelShufflePack.
        Args:
            x (Tensor): Input tensor with shape (in_channels, c, h, w).
        Returns:
            Tensor with shape (out_channels, c, scale_factor*h, scale_factor*w).
        """
        x = self.upsample_conv(x)
        x = self.pixel_shuffle(x)
        return x

@paddle.no_grad()
def default_init_weights(layer_list, scale=1, bias_fill=0, **kwargs):
    """Initialize network weights.
    Args:
        layer_list (list[nn.Layer] | nn.Layer): Layers to be initialized.
        scale (float): Scale initialized weights, especially for residual
            blocks. Default: 1.
        bias_fill (float): The value to fill bias. Default: 0
        kwargs (dict): Other arguments for initialization function.
    """
    if not isinstance(layer_list, list):
        layer_list = [layer_list]
    for m in layer_list:
        if isinstance(m, nn.Conv2D):
            kaiming_normal_(m.weight, **kwargs)
            scale_weight = scale * m.weight
            m.weight.set_value(scale_weight)
            if m.bias is not None:
                constant_(m.bias, bias_fill)
        elif isinstance(m, nn.Linear):
            kaiming_normal_(m.weight, **kwargs)
            scale_weight = scale * m.weight
            m.weight.set_value(scale_weight)
            if m.bias is not None:
                constant_(m.bias, bias_fill)
        elif isinstance(m, nn.BatchNorm):
            constant_(m.weight, 1)