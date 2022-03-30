"""
频谱分析 日
"""

import numpy as np
from scipy.fftpack import fft, fftfreq
from scipy.signal import periodogram, lombscargle, welch
from scipy import signal
import pandas as pd
import glob
from tqdm import tqdm
import matplotlib.pyplot as plt

import sys
sys.path.append('.')

from data.read_data import load_data

data_dir = "/Volumes/HDD/Data/ztd/"

# print(site_df.head())

from datetime import datetime

start = datetime(2010,1,2,0)

def lomb(idx, ts):
    tindex = idx.map(lambda x: (x - start).seconds/3600)
    t = np.arange(1, ts.shape[0]) # day 周期
    w = 2*np.pi/t
    # w = np.linspace(0.01, 8*np.pi/365, ts.shape[0])
    # t = 1/w * 2* np.pi
    pxx = lombscargle(tindex, ts, w, normalize=True)
    return t, pxx

def periodgram(idx, ts, fs):
    f, pxx = periodogram(ts, 1, return_onesided=True, detrend='linear', scaling='density')
    # f, pxx = welch(ts, 365, return_onesided=True, detrend='linear', scaling='spectrum')
    f = f[1:]
    pxx = pxx[1:]
    t = 1/f # * 365
    return t, pxx

# df = pd.read_csv(data_dir+"pwv_1h_hz_grl_filter.csv", index_col=0, parse_dates=True)
df = load_data(type='ztd', freq='h', fill=True)

sites = list(df.columns)

for site in sites:
    ts = df[site]
    tidx = ts.index
    b, a = signal.butter(8, 300, 'highpass', fs=int(24*365.25))
    filtedts = signal.filtfilt(b, a, ts)
    t, pxx = periodgram(tidx, filtedts, 1)
    # t, pxx = lomb(tidx, ts)
    plt.xlim(0, 2)
    plt.plot(t/24, pxx, color='black')
    # break
# plt.show()
plt.xlabel("Period")
plt.ylabel("PS")
plt.tight_layout()
plt.savefig("figs/psd-ztd-d.png")

