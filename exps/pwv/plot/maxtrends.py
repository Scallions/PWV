"""
最大最小趋势时间序列图
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import sys
sys.path.append(".")
from data.read_data import load_data
from gps.tools.detrend import detrend

df = load_data(type='pwv', freq='d', fill=True)

trends = pd.read_csv("dataset/trend.csv")
trends = trends.sort_values(by=['slope'])
trends = trends[trends['trend'] != 'no trend']
# print(trends)

site1 = trends['site'].values[0]
site2 = trends['site'].values[-1]

ts1 = df[site1]
ts2 = df[site2]

data1, b1 = detrend(ts1.index, ts1)
data2, b2 = detrend(ts2.index, ts2)
y_hat = np.dot(data1[:,:2], b1[:2])
# print(trends[trends['site'] == site1]['slope'].values[0], y_hat[-1]/12-y_hat[0]/12)

fig = plt.figure(dpi=300)
fig.set_figwidth(5)
fig.set_figheight(4)

ax = fig.add_subplot(2, 1, 1)
ax.set_ylabel(site1)
ax.plot(ts1)
ax.plot(ts1.index, np.dot(data1[:,:2], b1[:2]))
ax.plot(ts1.index, np.dot(data1[:,:4], b1[:4]))
ax.plot(ts1.index, np.dot(data1, b1))
ax.set_title(f" y={trends[trends['site'] == site1]['slope'].values[0]:.3f}x+{b1[0].item():.3f}", fontfamily='serif', loc='left', fontsize='medium', y=0.85)
ax1 = fig.add_subplot(2, 1, 2, sharex=ax)
ax1.set_ylabel(site2)
ax1.plot(ts2)
ax1.plot(ts2.index, np.dot(data2[:,:2], b2[:2]))
ax1.plot(ts2.index, np.dot(data2[:,:4], b2[:4]))
ax1.plot(ts2.index, np.dot(data2, b2))
ax1.set_title(f" y={trends[trends['site'] == site2]['slope'].values[0]:.3f}x+{b2[0].item():.3f}", fontfamily='serif', loc='left', fontsize='medium', y=0.85)

plt.tight_layout()
# plt.show()
plt.savefig("figs/maxtrends.png")