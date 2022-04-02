"""
计算残差
"""


import numpy as np
import pandas as pd
import glob
from tqdm import tqdm
import matplotlib.pyplot as plt
from scipy import signal
data_dir = "/Volumes/HDD/Data/ztd/"

import sys
sys.path.append('.')
from data.read_data import load_data
df = load_data(type='pwv', freq='h', fill=True)
# df = df[df.index.year < 2022]
# for fp in tqdm(glob.iglob(data_dir+"mete/*.csv"), total=total):
res = pd.DataFrame([], index=df.index, columns=df.columns)
for site in df.columns:
    # site_data = pd.read_csv(fp, parse_dates=['time'])
    ts = df[site]
    b, a = signal.butter(8, 800, 'highpass', fs=int(24*365.25))
    filtedts = signal.filtfilt(b, a, ts)
    res[site] = filtedts
    # plt.plot(ts.index, filtedts)
    # break
# plt.show()

res.to_csv(data_dir+"pwv_res.csv")
