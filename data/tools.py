

from typing import Tuple
import pandas as pd
import xarray as xr
import datetime

def load_gpspwv(fp: str) -> pd.DataFrame:
    """从fp位置读取gps pwv数据

    Args:
        fp (str): gps数据路径

    Returns:
        pd.DataFrame: pwv数据
    """
    df = pd.read_csv(fp, parse_dates=[0], index_col=[0])
    return df


def load_erapwv(fp: str) -> xr.DataArray:
    """加载era pwv数据

    Args:
        fp (str): 数据路径

    Returns:
        xr.DataArray: pwv数据
    """
    ds = xr.load_dataarray(fp)
    return ds

def common_data(gps: pd.DataFrame, era: xr.DataArray) -> Tuple[pd.DataFrame, xr.DataArray]:
    """提取gps和era中的公共观测时间段的数据

    Args:
        gps (pd.DataFrame): gps数据
        era (xr.DataArray): era数据

    Returns:
        Tuple[pd.DataFrame, xr.DataArray]: 公共观测时间段的gps和era数据
    """
    gps_common = gps.loc[gps.index.isin(era.time.values)]
    era_common = era.sel(time=gps_common.index)
    return gps_common, era_common

def time2mjd(dateT: datetime.datetime) -> float:
    """datetime转换为mjd

    Args:
        dateT (datetime.datetime): 时间

    Returns:
        float: mjd
    """
    t0=datetime.datetime(1858,11,17,0,0,0,0)#简化儒略日起始日
    mjd=(dateT-t0).days
    mjd_s=dateT.hour*3600.0+dateT.minute*60.0+dateT.second+dateT.microsecond/1000000.0
    return mjd+mjd_s/86400.0