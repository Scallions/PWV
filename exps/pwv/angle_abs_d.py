"""
计算相位和幅度
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
df = df[df.index.year < 2022]
stats = []
out_df = pd.DataFrame([], columns=['sitename', 'cons','linear','sinx','cosx','sin2x','cos2x'])
# for fp in tqdm(glob.iglob(data_dir+"mete/*.csv"), total=total):
for site in df.columns:
    # site_data = pd.read_csv(fp, parse_dates=['time'])
    ts = df[site]
    b, a = signal.butter(8, 300, 'highpass', fs=int(24*365.25))
    filtedts = signal.filtfilt(b, a, ts)
    hours = (ts.index - ts.index[0]).total_seconds() / 3600
    length = len(hours)
    x = hours.values.reshape((length, 1))
    sinx = np.sin(x * np.pi * 2 / 24)
    cosx = np.cos(x * np.pi * 2 / 24)
    sin2x = np.sin(2 * x * np.pi * 2 / 24)
    cos2x = np.cos(2 * x * np.pi * 2 / 24)
    ones = np.ones((length, 1))
    data = np.hstack((ones, x, sinx, cosx, sin2x, cos2x))
    b = np.dot(np.dot(np.linalg.inv(np.dot(data.transpose(), data)), data.transpose()), filtedts)
    out_df = out_df.append(pd.DataFrame([[site, b[0], b[1], b[2], b[3], b[4], b[5]]], columns=['sitename', 'cons','linear','sinx','cosx','sin2x','cos2x']))


out_df.to_csv("dataset/pwv_angle_abs_d.csv", index=False)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
fig = plt.figure(dpi=300)
ax = fig.add_subplot(projection="polar")
# plt.axhline(0)
# plt.axvline(0)
# plt.scatter(out_df['sinx'], out_df['cosx'], cmap='jet', c=out_df['year'], label='周年', alpha=0.5)
# plt.scatter(out_df['sin2x'], out_df['cos2x'], cmap='jet', c=out_df['year'], label='半周年', marker='x', alpha=0.5)

ang1 = np.angle(out_df['sinx'] + 1j * out_df['cosx'])
val1 = np.sqrt(out_df['sinx'] ** 2 + out_df['cosx'] ** 2)

ax.scatter(ang1, val1, cmap='jet', c=range(35), label='周日', alpha=0.5)

ang2 = np.angle(out_df['sin2x'] + 1j * out_df['cos2x'])
val2 = np.sqrt(out_df['sin2x'] ** 2 + out_df['cos2x'] ** 2)
c = ax.scatter(ang2, val2, cmap='jet', c=range(35), label='半周日', marker='x', alpha=0.5)
# plt.polar(ang1, val1, 'ro', label='周年', alpha=0.5)

# plt.hlines(0)
# plt.vlines(0)
plt.legend()
# plt.colorbar(c, ax=ax)
plt.tight_layout()
plt.savefig("figs/angle-pwv-h.png")
