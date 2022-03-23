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
tsafter = pd.read_csv(data_dir+"pwv_1d_hz_grl_filter_miss.csv", parse_dates=[0])
cols = list(tsafter.columns)
cols[0] = 'time'
tsafter.columns = cols
tsafter.set_index('time', inplace=True)


sitenames = tsbefore.isna().sum().sort_values(ascending=False).index
cnt = 7
size = 0.1
fig, ax = plt.subplots(cnt,1, sharex=True)
for i in range(cnt):
    sitename = sitenames[i]
    ax[i].scatter(tsafter.index, tsafter[sitename], label="fill", s=size)
    ax[i].scatter(tsbefore.index, tsbefore[sitename], label="raw", s=size)
    # plt.xlabel("Year")
    ax[i].set_ylabel(sitename)
    # plt.ylabel("ZTD/mm")
handles, labels = ax[i-1].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=5, bbox_to_anchor=(0.5, -0.01), markerscale=4, frameon=False)
plt.savefig("figs/pwv-missfill.png")