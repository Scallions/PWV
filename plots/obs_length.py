"""
站点数据观测量
"""

import pygmt
import pandas as pd
import sys
sys.path.append(".")
from data.filter_sites import greenland_sites

df = greenland_sites()
df = df.sort_values('Sta')
# print(df.tail())
# print(df.shape)
lossdf = pd.read_csv("./dataset/obs_length.csv")
lossdf = lossdf.sort_values('name')
lossdf.columns =['idx', "Sta", "len"]
df = pd.merge(df, lossdf, on=['Sta'])
# print(lossdf.tail())
# print(lossdf.shape)
# print(df.head())
# print(df.shape)

# exit()

fig = pygmt.Figure()

fig.basemap(region="-75/-10/55/86", projection="L-40/30/35/25/3i", frame=["x20", "y10"])
fig.coast(shorelines=True, water="white")
pygmt.makecpt(cmap="jet", series=[df.iloc[:,-1].min(),df.iloc[:,-1].max()])
fig.plot(
    x=df.iloc[:,2], # lon
    y=df.iloc[:,1], # lat
    style="c0.15c",
    color=df.iloc[:,-1],
    # color="black",
    cmap = True,
    pen="black"
)
fig.colorbar(frame=['x500'])
fig.savefig("figs/greenland_len.png")