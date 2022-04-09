
from abc import ABC, abstractclassmethod

class ITm(ABC):

    @abstractclassmethod
    def load_args(cls):
        raise NotImplementedError

    @abstractclassmethod
    def calc_tm(cls, lon, lat, year, doy, h):
        raise NotImplementedError

    @abstractclassmethod
    def calc_tm_year(cls, lon, lat, year, h):
        raise NotImplementedError

    @abstractclassmethod
    def calc_tm_dates(cls, lon:float, lat:float, dates, h:float):
        raise NotImplementedError