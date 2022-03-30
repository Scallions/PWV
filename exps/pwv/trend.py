"""
计算趋势项和周期项
"""


import numpy as np
import pandas as pd
import glob
from tqdm import tqdm
import matplotlib.pyplot as plt

data_dir = "/Volumes/HDD/Data/ztd/"

import sys
sys.path.append('.')
from data.read_data import load_data
df = load_data(type='pwv', freq='d', fill=True)

sites = list(df.columns)

out_df = pd.DataFrame([], columns=['sitename', 'cons','linear','sinx','cosx','sin2x','cos2x'])
res_df = pd.DataFrame([], columns=sites, index=df.index)
for site in sites:
    ts = df[site]
    ctidx = (ts.index - ts.index[0]).days
    length = len(ctidx)
    x = ctidx.values.reshape((length, 1))
    sinx = np.sin(x * np.pi * 2 / 365.25)
    cosx = np.cos(x * np.pi * 2 / 365.25)
    sin2x = np.sin(2 * x * np.pi * 2 / 365.25)
    cos2x = np.cos(2 * x * np.pi * 2 / 365.25)
    ones = np.ones((length, 1))
    data = np.hstack((ones, x, sinx, cosx, sin2x, cos2x))
    b = np.dot(np.dot(np.linalg.inv(np.dot(data.transpose(), data)), data.transpose()), ts)
    out_df = out_df.append(pd.DataFrame([[site, b[0], b[1], b[2], b[3], b[4], b[5]]], columns=['sitename', 'cons','linear','sinx','cosx','sin2x','cos2x']))
    y_hat = np.dot(data, b)
    res_df[site] = ts - y_hat
    # plt.plot(ts)
    # plt.plot(ts.index, y_hat)
    # plt.plot(ts.index, np.dot(data[:,:2], b[:2]))
    # plt.plot(ts.index, np.dot(data[:,:4], b[:4]))
    # plt.show()
    # break
out_df.to_csv("dataset/pwv_angle_abs_all.csv", index=False)
res_df.to_csv(data_dir+"pwv_1d_res_grl.csv", index=True)
