"""
原始的csv文件中只有时间、ztd、zwd、pwv、mt
在后面添加地面气压，水气压，地面气温
"""


import glob
from tqdm import tqdm as tqdm2
import pandas as pd
import xarray as xr
import os
from datetime import date, timedelta

import sys
sys.path.append(".")
from data.filter_sites import greenland_sites

data_dir = "/Volumes/HDD/Data/ztd/"
era_dir = "/Volumes/data3/era5/"

site_df = greenland_sites()

# print(site_df.head())

site_mete = {}

def pre_mete():
    # 判断还需要处理的站点
    sites = None
    for row in site_df.itertuples():
        sitename = row[1].lower()
        if os.path.exists(data_dir+"mete/"+sitename+".csv"):
            continue
        if sites is None:
            sites = site_df.iloc[row[0]:row[0]+1,:]
        else:
            sites = sites.append(site_df.iloc[row[0]:row[0]+1,:])
        # sites.add(sitename)


    # 遍历 era5 文件

    start = sites['Dtbeg'].min()
    start = date(*[int(i) for i in start.split('-')])
    # start = date(2011,9,25)
    end = date(2020, 1, 1)

    cur  = start
    total = (end-start).days
    process_bar = tqdm2(total=total)
    pres_df = pd.DataFrame([], columns=[name.lower() for name in list(sites['Sta'])])
    es_df = pd.DataFrame([], columns=[name.lower() for name in list(sites['Sta'])])
    rhs_df = pd.DataFrame([], columns=[name.lower() for name in list(sites['Sta'])])
    ts_df = pd.DataFrame([], columns=[name.lower() for name in list(sites['Sta'])])
    while cur < end:
        year = cur.year
        mon = cur.month
        day = cur.day
        doy = cur.timetuple().tm_yday
        pres_cur = pd.DataFrame([], columns=[name.lower() for name in list(sites['Sta'])], index=[cur])
        es_cur = pd.DataFrame([], columns=[name.lower() for name in list(sites['Sta'])], index=[cur])
        rhs_cur = pd.DataFrame([], columns=[name.lower() for name in list(sites['Sta'])], index=[cur])
        ts_cur = pd.DataFrame([], columns=[name.lower() for name in list(sites['Sta'])], index=[cur])
        era_fp = era_dir + f"{year}/era5_{year}_{mon}_{day}.nc"
        if not os.path.exists(era_fp):
            cur += timedelta(1)
            process_bar.update()
        era5_ds = xr.open_dataset(era_fp).mean('time')
        for row in sites.itertuples():
            sitename = row[1].lower()
            lon = row[3]-360
            lat = row[2]
            h = row[4]
            era_ds = era5_ds.interp(longitude=lon, latitude=lat)
            rhs = era_ds.r
            ts = era_ds.t
            hs = era_ds.z / 9.7803253359
            level = era_ds.level
            ls = xr.DataArray(level.values, coords=[hs.values], dims="h")
            if h < hs.min():
                dh = (hs[36]-h)/(hs[35]-hs[36])
                l = level[36]+dh*(level[36]-level[35])
                temp = ts[36]+dh*(ts[36]-ts[35])-273.15
                rh = rhs[36]+dh*(rhs[36]-rhs[35])
            else:
                try:
                    l = ls.interp(h=h)
                    temp = ts.interp(level=l)-273.15
                    rh = rhs.interp(level=l)
                except:
                    print(h, hs)
                    # pres_cur[sitename] = l.item()
                    # es_cur[sitename] = e.item()
                    # rhs_cur[sitename] = rh.item()
                    # ts_cur[sitename] = temp.item()
                    continue
            es = 6.11*10**(7.5*temp/(237.3+temp))
            e = rh*es/100
            pres_cur[sitename] = l.item()
            es_cur[sitename] = e.item()
            rhs_cur[sitename] = rh.item()
            ts_cur[sitename] = temp.item()
        pres_df = pres_df.append(pres_cur)
        es_df = es_df.append(es_cur)
        rhs_df = rhs_df.append(rhs_cur)
        ts_df = ts_df.append(ts_cur)
        # break

        cur += timedelta(1)
        process_bar.update()
    rhs_df.index = pd.DatetimeIndex(rhs_df.index)
    pres_df.index = pd.DatetimeIndex(pres_df.index)
    es_df.index = pd.DatetimeIndex(es_df.index)
    ts_df.index = pd.DatetimeIndex(ts_df.index)
    # 遍历站点添加站点信息
    for row in sites.itertuples():
        sitename = row[1].lower()
        lon = row[3]-360
        lat = row[2]
        h = row[4]
        fp = data_dir+f"all/{sitename.upper()}.csv"
        if not os.path.exists(fp):
            continue
        site_data = pd.read_csv(fp, parse_dates=[1])
        site_data = site_data.set_index('time')
        site_data = pd.DataFrame(site_data.resample('1D').mean()).dropna()
        vidx = rhs_df.index & site_data.index
        site_data['lon'] = [lon]*site_data.shape[0]
        site_data['lat'] = [lat]*site_data.shape[0]
        site_data['h'] = [h]*site_data.shape[0]
        site_data.loc[vidx, 'rh'] = rhs_df.loc[vidx][sitename]
        site_data.loc[vidx, 'e'] = es_df.loc[vidx][sitename]
        site_data.loc[vidx, 'T'] = ts_df.loc[vidx][sitename]
        site_data.loc[vidx, 'p'] = pres_df.loc[vidx][sitename]
        site_data.to_csv(data_dir+"mete/"+sitename+".csv")

def process_fp(fp):
    # print(fp)
    sitename = fp.split("/")[-1][:4]
    # print(sitename)
    # print(site_df.columns)
    siteinfo = site_df[site_df["Sta"]==sitename]
    # print(siteinfo, siteinfo.shape)
    if siteinfo.shape[0] == 0:
        return
    lat = siteinfo["Lat(deg)"].item()
    lon = siteinfo["Long(deg)"].item()-360
    h = siteinfo["Hgt(m)"].item()
    # print(lon, lat, h)
    # 读取并重采样为一天
    site_data = pd.read_csv(fp, parse_dates=[1])
    site_data = site_data.set_index('time')
    site_data = pd.DataFrame(site_data.resample('1D').mean()).dropna()
    if 'Unnamed: 0' in site_data.columns:
        site_data = site_data.drop(labels='Unnamed: 0', axis=1)
    Pres = []
    Rhs = []
    Es = []
    Ts = []
    if os.path.exists(data_dir+"mete/"+sitename+".csv"):
        return
    for row in tqdm2(site_data.itertuples(), leave=False, total=site_data.shape[0]):
    # for row in site_data.itertuples():
        # print(row)
        t = row[0]
        year = t.year
        mon = t.month
        day = t.day
        era_fp = era_dir + f"{year}/era5_{year}_{mon}_{day}.nc"
        if year > 2019 or not os.path.exists(era_fp):
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
            l = level[36]+dh*(level[36]-level[35])
            temp = ts[36]+dh*(ts[36]-ts[35])-273.15
            rh = rhs[36]+dh*(rhs[36]-rhs[35])
        else:
            try:
                l = ls.interp(h=h)
                temp = ts.interp(level=l)-273.15
                rh = rhs.interp(level=l)
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
        Pres.append(l.item())
        Rhs.append(rh.item())
        Es.append(e.item())
        Ts.append(temp.item())
    site_data['lon'] = [lon]*site_data.shape[0]
    site_data['lat'] = [lat]*site_data.shape[0]
    site_data['h'] = [h]*site_data.shape[0]
    site_data['rh'] = Rhs
    site_data['e'] = Es
    site_data['T'] =Ts
    site_data['p'] = Pres
    site_data.to_csv(data_dir+"mete/"+sitename+".csv")
    # break

pre_mete()

# for fp in tqdm2(glob.glob(data_dir+"all/*.csv")):
#     process_fp(fp)

# 开多进程加速 有bug
# from multiprocessing import Pool
# total = len(glob.glob(data_dir+"all/*.csv"))
# with Pool(10) as pool:
#      for i in tqdm2(pool.imap(process_fp, glob.iglob(data_dir+"all/*.csv")), total=total):
#          pass

#import tqdm.contrib.concurrent
#tqdm.contrib.concurrent.process_map(process_fp, glob.glob(data_dir+"all/*.csv"))
