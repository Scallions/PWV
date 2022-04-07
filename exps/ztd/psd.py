"""
频谱分析
"""

import numpy as np
from scipy.fftpack import fft, fftfreq
from scipy.signal import periodogram, lombscargle, welch
import pandas as pd
import glob
from tqdm import tqdm
import matplotlib.pyplot as plt

data_dir = "/Volumes/HDD/Data/ztd/"

# print(site_df.head())


def lomb(idx, ts):
    start = idx[0]
    tindex = idx.map(lambda x: (x - start).days)
    # t = np.arange(1, ts.shape[0]) # day 周期
    t = np.arange(1, 365*2)
    w = 2*np.pi/t
    # w = np.linspace(0.01, 8*np.pi/365, ts.shape[0])
    # t = 1/w * 2* np.pi
    pxx = lombscargle(tindex, ts, w, normalize=True)
    return t, pxx

def periodgram(idx, ts):
    f, pxx = periodogram(ts, 1, return_onesided=True, detrend='linear', scaling='density')
    # f, pxx = welch(ts, 365, return_onesided=True, detrend='linear', scaling='spectrum')
    f = f[1:]
    pxx = pxx[1:]
    t = 1/f # * 365
    return t, pxx

total = len(glob.glob(data_dir+"mete/*.csv"))
stats = []
fig = plt.figure(dpi=300)
fig.set_figwidth(5)
fig.set_figheight(3)
for fp in tqdm(glob.iglob(data_dir+"mete/*.csv"), total=total):
    sitename = fp.split("/")[-1][:4]
    site_data = pd.read_csv(fp, parse_dates=['time'])
    ts = site_data['ztd']
    ts = ts - ts.mean()
    ts = ts.values
    if len(ts) < 365:
        continue
    start = site_data['time'][0]
    tindex = site_data['time'].map(lambda x: (x - start).days)
    # y_hat = fft(ts)
    # y_abs = np.abs(y_hat)
    # y_angle = np.angle(y_hat)

    # fs = 365
    # xf = fftfreq(ts.shape[0], 1/fs)
    # xf[1:] = 1/xf[1:] * 365
    # plt.plot(xf[1: ts.shape[0]//2], 2.0/ ts.shape[0] * y_abs[1: ts.shape[0]//2])
    # plt.savefig("figs/psd1.png")
    # plt.figure()
    # plt.psd(ts, 512, 365)
    # plt.savefig("figs/psd2.png")

    # f, pxx = periodogram(ts, 365, return_onesided=True, detrend='linear', scaling='density')
    # # f, pxx = welch(ts, 365, return_onesided=True, detrend='linear', scaling='spectrum')
    # f = f[1:]
    # pxx = pxx[1:]
    # t = 1/f # * 365
    # plt.figure()
    # t,pxx = lomb(site_data['time'], ts)
    t, pxx = periodgram(site_data['time'], ts)
    plt.plot(t, pxx, color='black')
    plt.xlim(0,1000)
    # plt.semilogy(t, pxx)
    # fig, (ax_t, ax_w) = plt.subplots(2, 1, constrained_layout=True)
    # ax_t.plot(tindex, ts)
    # ax_w.plot(t, pxx)
    # break

plt.xlabel("Period(day)")
plt.ylabel("PS")
plt.tight_layout()
plt.savefig("figs/psd-ztd.png")

