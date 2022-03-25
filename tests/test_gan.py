import pytest

import paddle

from model.dcgenerator import DCGenerator

class TestGAN:

    def test_shape(self):
        b = 3
        inp = paddle.randn([b,35])
        gan = DCGenerator(35, 1)
        out = gan(inp)
        assert out.shape == [b,31,66]
        # assert 1 == 1