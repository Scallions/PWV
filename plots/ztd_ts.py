import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta, datetime

datasetdir = "/Volumes/HDD/Data/ztd/"

fp = datasetdir + "all/KSNB.csv"

df = pd.read_csv(fp, parse_dates=[1])
df = df.set_index('time')
# print(df.shape)
# ztd = df['ztd'].resample('1D')
# ztd = pd.DataFrame(ztd)
# print(len(ztd))
# print(ztd.columns)
# print(ztd.head())

df = pd.DataFrame(df.resample('1D').mean())
print(df.head())

plt.figure()
# ztd.plot()
plt.plot(df["zwd"])
# plt.show()

plt.savefig("figs/siteztd.png")