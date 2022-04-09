import pytest

from gps.libs import manager
from gps.tm import pca

class TestManager:

    def test_tm(self):
        tms = manager.TM_MODELS
        cps = tms.components_dict
        name = tms.name
        assert name == 'TM_MODELS'
        assert 'PCA' in cps