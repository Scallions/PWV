"""
GPT3模型
"""

from .itm import ITm

import xarray as xr
import numpy as np

from gps.libs import manager

@manager.TM_MODELS.add_component
class GPT3(ITm):
    name = "GPT3"
    args = None

    @classmethod
    def load_args(cls):
        if cls.args is None:
            cls.args = xr.load_dataarray("./dataset/gpt3-tm-args2.nc")

    @classmethod
    def calc_tm(cls, lon, lat, year, doy, h):
        """模型计算Tm，采用的主要是sin cos周期建模，加上高度改正

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
        cargs = cls.args.interp(lon=lon, lat=lat)
        x = np.array([1, np.cos(doy* np.pi * 2 / 365.25), np.sin(doy* np.pi * 2 / 365.25), np.cos(2*doy* np.pi * 2 / 365.25), np.sin(2*doy* np.pi * 2 / 365.25)])
        tm = np.dot(cargs, x)
        return tm

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
        args = cls.args.interp(lon=lon, lat=lat)
        doy = np.arange(0,365)
        x = x = np.array([np.ones_like(doy), np.cos(doy* np.pi * 2 / 365), np.sin(doy* np.pi * 2 / 365), np.cos(2*doy* np.pi * 2 / 365), np.sin(2*doy* np.pi * 2 / 365)])
        tm = np.dot(args, x)
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
        args = cls.args.interp(lon=lon, lat=lat)
        doy = dates.doy
        x = x = np.array([np.ones_like(doy), np.cos(doy* np.pi * 2 / 365), np.sin(doy* np.pi * 2 / 365), np.cos(2*doy* np.pi * 2 / 365), np.sin(2*doy* np.pi * 2 / 365)])
        tm = np.dot(args, x)
        return tm
