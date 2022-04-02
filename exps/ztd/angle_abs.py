"""
计算相位和幅度
"""


import numpy as np
import pandas as pd
import glob
from tqdm import tqdm
import matplotlib.pyplot as plt

data_dir = "/Volumes/HDD/Data/ztd/"


total = len(glob.glob(data_dir+"mete/*.csv"))
stats = []
out_df = pd.DataFrame([], columns=['sitename', 'lon', 'lat', 'h', 'year', 'cons','linear','sinx','cosx','sin2x','cos2x'])
for fp in tqdm(glob.iglob(data_dir+"mete/*.csv"), total=total):
    sitename = fp.split("/")[-1][:4]
    site_data = pd.read_csv(fp, parse_dates=['time'])
    lon = site_data['lon'].values[0]
    lat = site_data['lat'].values[0]
    h = site_data['h'].values[0]
    ts = site_data['ztd']
    ts = ts - ts.mean()
    ts = ts.values
    # start = site_data['time'][0]
    # tindex = site_data['time'].map(lambda x: (x - start).days)
    tidx = pd.DatetimeIndex(site_data['time'])
    start_year = tidx[0].year
    end_year = tidx[-1].year
    for year in range(start_year, end_year+1):
        cnt = (tidx.year == year).sum()
        if cnt < 360:
            continue
        cts = ts[tidx.year == year]
        ctidx = tidx[tidx.year == year].day_of_year
        length = len(ctidx)
        x = ctidx.values.reshape((length, 1))
        sinx = np.sin(x * np.pi * 2 / 365)
        cosx = np.cos(x * np.pi * 2 / 365)
        sin2x = np.sin(2 * x * np.pi * 2 / 365)
        cos2x = np.cos(2 * x * np.pi * 2 / 365)
        ones = np.ones((length, 1))
        data = np.hstack((ones, x, sinx, cosx, sin2x, cos2x))
        b = np.dot(np.dot(np.linalg.inv(np.dot(data.transpose(), data)), data.transpose()), cts)
        out_df = out_df.append(pd.DataFrame([[sitename, lon, lat, h, year, b[0], b[1], b[2], b[3], b[4], b[5]]], columns=['sitename', 'lon', 'lat', 'h', 'year', 'cons','linear','sinx','cosx','sin2x','cos2x']))


out_df.to_csv("dataset/ztd_angle_abs.csv", index=False)
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

ax.scatter(ang1, val1, cmap='jet', c=out_df['year'], label='周年', alpha=0.5)

ang2 = np.angle(out_df['sin2x'] + 1j * out_df['cos2x'])
val2 = np.sqrt(out_df['sin2x'] ** 2 + out_df['cos2x'] ** 2)
c = ax.scatter(ang2, val2, cmap='jet', c=out_df['year'], label='半周年', marker='x', alpha=0.5)
# plt.polar(ang1, val1, 'ro', label='周年', alpha=0.5)

# plt.hlines(0)
# plt.vlines(0)
plt.legend()
plt.colorbar(c, ax=ax)
# plt.show()
plt.tight_layout()
plt.savefig("figs/angle-ztd.png")
