"""
原始的csv文件中只有时间、ztd、zwd、pwv、mt
在后面添加地面气压，水气压，地面气温
"""


import glob
from tqdm import tqdm
import pandas as pd
import xarray as xr
import os

import sys
sys.path.append(".")
from data.filter_sites import greenland_sites

data_dir = "/Volumes/HDD/Data/ztd/"
era_dir = "/Volumes/data3/era5/"

site_df = greenland_sites()

# print(site_df.head())


for fp in tqdm(glob.iglob(data_dir+"all/*.csv")):
    # print(fp)
    sitename = fp.split("/")[-1][:4]
    # print(sitename)
    # print(site_df.columns)
    siteinfo = site_df[site_df["Sta"]==sitename]
    # print(siteinfo, siteinfo.shape)
    lat = siteinfo["Lat(deg)"].item()
    lon = siteinfo["Long(deg)"].item()-360
    h = siteinfo["Hgt(m)"].item()
    # print(lon, lat, h)
    # 读取并重采样为一天
    site_data = pd.read_csv(fp, parse_dates=[1])
    site_data = site_data.set_index('time')
    site_data = pd.DataFrame(site_data.resample('1D').mean())
    Pres = []
    Rhs = []
    Es = []
    Ts = []
    for row in tqdm(site_data.itertuples(), total=site_data.shape[0], leave=False):
        # print(row)
        t = row[0]
        year = t.year
        mon = t.month
        day = t.day
        era_fp = era_dir + f"{year}/era5_{year}_{mon}_{day}.nc"
        if not os.path.exists(era_fp):
            Pres.append(None)
            Es.append(None)
            Rhs.append(None)
            Ts.append(None)
            continue
        era_ds = xr.open_dataset(era_fp).mean('time').interp(longitude=lon, latitude=lat)
        rhs = era_ds.r
        ts = era_ds.t
        hs = era_ds.z / 9.7803253359
        level = era_ds.level
        ls = xr.DataArray(level.values, coords=[hs.values], dims="h")
        if h < hs.min():
            dh = (hs[36]-h)/(hs[35]-hs[36])
            l = level[36]+dh*(level[36]-level[35]).item()
            temp = ts[36]+dh*(ts[36]-ts[35]).item()-273.15
            rh = rhs[36]+dh*(rhs[36]-rhs[35]).item()
        else:
            try:
                l = ls.interp(h=h).item()
                temp = ts.interp(level=l).item()-273.15
                rh = rhs.interp(level=l).item()
            except:
                print(h, hs)
                Pres.append(None)
                Es.append(None)
                Rhs.append(None)
                Ts.append(None)
                continue
        es = 6.11*10**(7.5*temp/(237.3+temp))
        e = rh*es/100
        # print(year, mon, day, h, l, temp, rh, e)
        Pres.append(l)
        Rhs.append(rh)
        Es.append(e)
        Ts.append(temp)
    site_data['rh'] = rh
    site_data['e'] = Es
    site_data['T'] =Ts
    site_data['p'] = Pres
    site_data.to_csv(data_dir+"mete/"+sitename+".csv")
    break