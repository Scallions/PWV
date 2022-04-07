"""
累积可降雨量
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

ts = ts.groupby(ts.index.year).sum()

data_dir = "/Volumes/HDD/Data/ztd/"
df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl_filter.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13]))
ts = ts[df['Sta']]
ts = ts.iloc[:-1,:]

import pygmt

pygmt.config(MAP_TITLE_OFFSET="1p")
pygmt.config(MAP_HEADING_OFFSET="1p")

maxi = ts.idxmax(axis=1)
mini = ts.idxmin(axis=1)
print(maxi, mini)

pmin = ts.min().min()-1
pmax = ts.max().max()+1
print(pmin, pmax)
start = 2010
end = 2021
fig = pygmt.Figure()
with fig.subplot(nrows = 4, ncols = 3, figsize=("20c", "30c"), autolabel="(a)+o0c/-0.3c", margins=["0.1c", "1c"]):
    for year in range(start, end+1):
        i = year -start
        row = i // 3
        col = i % 3
        psum = ts[ts.index == year].values[0,:]

        # fig.shift_origin(yshift="h-1c")
        with fig.set_panel(panel=[row, col]):
            fig.basemap(region="-75/-10/55/86", projection="L-42.5/30/35/25/2i", frame=["x20", "y10", f"+t{year}"])
            fig.coast(region="-75/-10/55/86", projection="L-42.5/30/35/25/2i",shorelines=True, water="white")
            pygmt.makecpt(cmap="jet", series=[pmin, pmax])
            fig.plot(region="-75/-10/55/86", projection="L-42.5/30/35/25/2i",
                x=df.iloc[:,2], # lon
                y=df.iloc[:,1], # lat
                style="c0.2c",
                color=psum,
                # color="black",
                cmap = True,
                pen="black"
            )
pygmt.makecpt(cmap="jet", series=[pmin, pmax])
fig.colorbar(position="+jLB+h+w6c+o5.8c/-1c", frame=['x'])
fig.savefig(f"figs/pwv_sum_gird.png")