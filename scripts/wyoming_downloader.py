"""
利用siphon下载wyoming探空数据
"""

import pandas as pd
from datetime import datetime, timedelta
from metpy.units import units

from siphon.simplewebservice.wyoming import WyomingUpperAir


# date = datetime(2022, 3, 16, 0)
# station = 'ABQ'
# df = WyomingUpperAir.request_data(date, station)
# print(df.columns)
# print(df.head())
# print(df['RELH'])


# df, header = IGRAUpperAir.request_data(date, station)

data_dir = "/Volumes/HDD/Data/radio/recalc"

siteinfo = pd.read_csv("dataset/radio.csv", sep=r"\s+", header=None)
print(siteinfo.head())

from tqdm import tqdm

for row in tqdm(siteinfo.itertuples(), total=siteinfo.shape[0]):
    start_year = row[4]
    end_year = row[5]
    if end_year < 1973:
        continue
    start_year = max(1973, start_year)
    sitename = f"{row[1]:05d}"
    # print(start_year, end_year, sitename)
    start = datetime(start_year, 1, 1)
    if end_year < 2022:
        end = datetime(end_year, 12, 31)
    else:
        end = datetime(2022, 3, 16)
    days = (end - start).days
    for dt in tqdm(range(days), total=days, position=2, leave=False, desc=sitename):
        date = start + timedelta(days=dt)
        try:
            df = WyomingUpperAir.request_data(date, sitename)
        except ValueError:
            continue
        if df is not None:
            df.to_csv(f"{data_dir}/{sitename}_{date.strftime('%Y%m%d')}.csv", index=False)
            # print(df.head())