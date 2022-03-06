"""
pwv时间序列图，单站点
"""
import sys
sys.path.append(".")

import pandas as pd
import matplotlib.pyplot as plt

import gps.ztd.zhd.saas
import gps.pwv.pwv

datasetdir = "/Volumes/HDD/Data/ztd/"

fp = datasetdir + "mete/SRMP.csv"

df = pd.read_csv(fp, parse_dates=[1])
df = df.set_index('time')
df['ztd'] = df['ztd'].astype(float)

zhd = gps.ztd.zhd.saas.saas(df["lat"], df["p"], df["h"]) * 1000

print(df.head())
print(df.info())
gpszhd = df["ztd"]-df["zwd"]
zwd = df["ztd"] - zhd
pwv = gps.pwv.pwv.pwv(zwd, df["mt"])

plt.figure()
# ztd.plot()
# plt.plot(df["pwv"])
# gpszhd.plot(label="gps")
# zhd.plot(label="era")
pwv.plot()

dzhd = gpszhd-zhd
print(dzhd.describe())
# plt.show()
plt.legend()
plt.savefig("figs/pwv.png")