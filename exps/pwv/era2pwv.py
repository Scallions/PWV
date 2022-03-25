"""
使用era5计算iwv
"""


import xarray as xr
from tqdm import tqdm
from datetime import date, timedelta
import numpy as np
import os
era_dir = "/Volumes/data3/era5"
data_dir = "/Volumes/HDD/Data/ztd/pwv"


Rd = 287.058
g0 = 9.80665
start = 2010
end = 2019

for year in tqdm(range(start, end+1)):
    sday = date(year, 1, 1)
    eday = date(year, 12, 31)
    days = (eday-sday).days+1
    for i in tqdm(range(days), leave=False):
        cur = sday + timedelta(days=i)
        mon = cur.month
        day = cur.day
        if os.path.exists(f"{data_dir}/{year}/era5_pwv_{year}_{mon}_{day}.nc"):
            continue
        fp = f"{era_dir}/{year}/era5_{year}_{mon}_{day}.nc"
        ds = xr.load_dataset(fp)
        alt = ds.z / g0 # t, z, lat , lon m
        rhs = ds.r # %
        pres = ds.level # 巴 转 hpa
        tempk = ds.t  # 开式温度
        tempc = tempk - 273.15 # 摄氏温度
        e_sat = 6.112*np.exp((17.62*tempc)/(tempc+243.12))
        var_pres = rhs * e_sat / 100
        p_dry = 100/(Rd*tempk)*pres
        mix_rat = 0.622*var_pres/(-var_pres+pres)
        cwv = (mix_rat[:,1:,:,:]*p_dry[:,1:,:,:]) * (-alt[:,1:,:,:] + alt[:,:-1,:,:].values)
        pwv = cwv.sum(axis=1)/997*1000
        # print(fp)201
        pwv.to_netcdf(f"{data_dir}/{year}/era5_pwv_{year}_{mon}_{day}.nc")
    #     break
    # break