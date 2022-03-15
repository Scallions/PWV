"""
频谱分析
"""

import numpy as np
from scipy.fftpack import fft, fftfreq
from scipy.signal import periodogram
import pandas as pd
import glob
from tqdm import tqdm
import matplotlib.pyplot as plt

data_dir = "/Volumes/HDD/Data/ztd/"

# print(site_df.head())

total = len(glob.glob(data_dir+"mete/*.csv"))
stats = []
for fp in tqdm(glob.iglob(data_dir+"mete/*.csv"), total=total):
    sitename = fp.split("/")[-1][:4]
    site_data = pd.read_csv(fp)
    ts = site_data['ztd']
    ts = ts - ts.mean()
    ts = ts.values
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

    f, pxx = periodogram(ts, 365, return_onesided=True, detrend='linear', scaling='density')
    f = f[1:]
    pxx = pxx[1:]
    t = 1/f # * 365
    # plt.figure()
    plt.plot(t, pxx)
    # plt.semilogy(t, pxx)

plt.xlabel("Period")
plt.ylabel("PS")
plt.savefig("figs/psd-ztd.png")
    # break
