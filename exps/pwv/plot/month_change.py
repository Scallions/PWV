"""

绘制pwv时间序列图

"""
import pandas as pd
import matplotlib.pyplot as plt

data_dir = "/Volumes/HDD/Data/ztd/"
tsbefore = pd.read_csv(data_dir+"pwv_1d_hz_grl_filter.csv", parse_dates=[0])
cols = list(tsbefore.columns)
cols[0] = 'time'
tsbefore.columns = cols
tsbefore.set_index('time', inplace=True)
ts = pd.read_csv(data_dir+"pwv_1d_hz_grl_filter_miss.csv", parse_dates=[0])
cols = list(ts.columns)
cols[0] = 'time'
ts.columns = cols
ts.set_index('time', inplace=True)

ts = ts.groupby(ts.index.month).mean()


sitenames = tsbefore.isna().sum().sort_values(ascending=False).index
cnt = 7
size = 0.1
fig, ax = plt.subplots(cnt,1, sharex=True)
for i in range(cnt):
    sitename = sitenames[i]
    ax[i].plot(ts.index, ts[sitename])
    ax[i].scatter(ts.index, ts[sitename], s=size)
    # plt.xlabel("Year")
    ax[i].set_ylabel(sitename)
    # plt.ylabel("ZTD/mm")
# handles, labels = ax[i-1].get_legend_handles_labels()
# fig.legend(handles, labels, loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.01), markerscale=4, frameon=False)
plt.savefig("figs/pwv-month.png")
# print(ts.head())