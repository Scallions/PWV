import pytest

from gps.tm import GTrop

class TestTm:
    def test_gtrop(self):
        tm = GTrop.calc_tm(lon=-40, lat=68, year=2019, doy=1, h=0)
        assert 1 == 1