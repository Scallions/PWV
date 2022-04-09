"""
GTrop模型
"""


# from imodel import IModel

import xarray as xr
import numpy as np

from gps.libs import manager

from .itm import ITm
@manager.TM_MODELS.add_component
class GTrop(ITm):
    name = "GTrop"
    Targs = None
    Dtargs = None
    H = None

    @classmethod
    def load_args(cls):
        if cls.Targs is None:
            cls.Targs = xr.load_dataarray("dataset/gtrop_tm_grl.nc")
            cls.Dtargs = xr.load_dataarray("dataset/gtrop_dt_grl.nc")
            cls.H = xr.load_dataarray("dataset/gtrop_h.nc")

    @classmethod
    def calc_tm(cls, lon, lat, year, doy, h):
        """GTrop模型计算Tm，采用的主要是sin cos周期建模，加上高度改正

        Args:
            lon (float): 经度
            lat (float): 维度
            year (int): 年份
            doy (int): 年积日
            h (float): 高度

        Returns:
            float: 对应位置、时间、高度的加权平均温度
        """
        cls.load_args()
        args = cls.Targs.interp(longitude=lon, latitude=lat)
        dtargs = cls.Dtargs.interp(longitude=lon, latitude=lat)
        hs = cls.H.interp(longitude=lon, latitude=lat)
        Tr = year + doy/365.25 - 1980
        C1 = np.cos(doy*2*np.pi/365.25)
        S1 = np.sin(doy*2*np.pi/365.25)
        C2 = np.cos(doy*4*np.pi/365.25)
        S2 = np.sin(doy*4*np.pi/365.25)
        xs = np.stack([Tr, 1, C1, S1, C2, S2])
        tm = np.dot(args, xs)
        rate = np.dot(dtargs, xs)
        tm = tm + rate*(hs-h)/1000
        return tm.item()

    @classmethod
    def calc_tm_year(cls, lon, lat, year, h):
        """计算整年的Tm时间序列，相较于单次计算，采用矩阵可以加快计算速度

        Args:
            lon (float): 经度
            lat (float): 维度
            year (int): 年
            h (float): 高度

        Returns:
            np.ndarray: Tm时间序列
        """
        cls.load_args()
        args = cls.Targs.interp(longitude=lon, latitude=lat)
        dtargs = cls.Dtargs.interp(longitude=lon, latitude=lat)
        hs = cls.H.interp(longitude=lon, latitude=lat)
        # TODO: 根据每年计算相应的doy数量，目前为365
        doy = np.arange(0,365).reshape((365,))
        Tr = year + doy/365.25 - 1980
        C1 = np.cos(doy*2*np.pi/365.25)
        S1 = np.sin(doy*2*np.pi/365.25)
        C2 = np.cos(doy*4*np.pi/365.25)
        S2 = np.sin(doy*4*np.pi/365.25)
        xs = np.stack([Tr, np.ones_like(Tr), C1, S1, C2, S2])
        tm = np.dot(args, xs)
        rate = np.dot(dtargs, xs)
        tm = tm + rate*(hs-h)/1000
        return tm


    @classmethod
    def calc_tm_dates(cls, lon:float, lat:float, dates, h:float)->np.ndarray:
        """根据dates中的日期，指定地点的tm

        Args:
            lon (float): 经度
            lat (float): 纬度
            dates (_type_): 需要计算的一些日期
            h (float): 高度

        Returns:
            np.ndarray: 计算所得的tm
        """
        cls.load_args()
        args = cls.Targs.interp(longitude=lon, latitude=lat)
        dtargs = cls.Dtargs.interp(longitude=lon, latitude=lat)
        # 构建系数矩阵 TODO: 具体实现
        year = dates.year
        doy = dates.doy
        # 计算地面Tm
        hs = cls.H.interp(longitude=lon, latitude=lat)
        Tr = year + doy/365.25 - 1980
        C1 = np.cos(doy*2*np.pi/365.25)
        S1 = np.sin(doy*2*np.pi/365.25)
        C2 = np.cos(doy*4*np.pi/365.25)
        S2 = np.sin(doy*4*np.pi/365.25)
        xs = np.stack([Tr, np.ones_like(Tr), C1, S1, C2, S2])
        tm = np.dot(args, xs)
        rate = np.dot(dtargs, xs)
        # 计算高度h处Tm
        tm = tm + rate*(hs-h)/1000
        return tm



if __name__ == '__main__':
    test = GTrop() # 得生成对象才能检测有没有实现类方法
    lon = -60
    lat = 60
    year = 2019
    doy = 200
    h = 1000
    tm = GTrop.calc_tm(lon, lat, year, doy, h)
    print(tm)
    tms = GTrop.calc_tm_year(lon, lat, year, h)
    print(tms.shape, tms.mean(), type(tms))