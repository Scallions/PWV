"""
计算相位和幅度
"""


import numpy as np
import pandas as pd
import glob
from tqdm import tqdm
import matplotlib.pyplot as plt
from datetime import datetime

data_dir = "/Volumes/HDD/Data/ztd/"


# total = len(glob.glob(data_dir+"mete/*.csv"))
tsc = pd.read_csv(data_dir+"all_r/pwv_1h_hz_grl_long_fill.csv", parse_dates=['time'])
stats = []
sites = tsc.columns[1:]
out_df = pd.DataFrame([], columns=['sitename', 'cons','linear','sinx','cosx','sin2x','cos2x'])
start = datetime(2010,1,1)
tidx = pd.DatetimeIndex(tsc['time'])
days = (tidx-start).total_seconds()/86400
length = len(days)
tso = tsc.copy()
for site in sites:
    ts = tsc[site]
    # ts = ts - ts.mean()
    ts = ts.values
    # start = site_data['time'][0]
    # tindex = site_data['time'].map(lambda x: (x - start).days)
    x = days.values.reshape((length, 1))
    sinx = np.sin(x * np.pi * 2 / 365.25)
    cosx = np.cos(x * np.pi * 2 / 365.25)
    sin2x = np.sin(2 * x * np.pi * 2 / 365.25)
    cos2x = np.cos(2 * x * np.pi * 2 / 365.25)
    ones = np.ones((length, 1))
    data = np.hstack((ones, x, sinx, cosx, sin2x, cos2x))
    b = np.dot(np.dot(np.linalg.inv(np.dot(data.transpose(), data)), data.transpose()), ts)
    out_df = out_df.append(pd.DataFrame([[site, b[0], b[1], b[2], b[3], b[4], b[5]]], columns=['sitename', 'cons','linear','sinx','cosx','sin2x','cos2x']))
    tso[site] = tso[site] - np.dot(data, b)

out_df.to_csv(data_dir + "all_r/trends.csv", index=False)
tso.to_csv(data_dir + "all_r/remove_trend.csv", index=False)
