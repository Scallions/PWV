"""
所有gps站点的位置图
带名字
"""

import pygmt
import pandas as pd
import sys
sys.path.append(".")
from data.filter_sites import greenland_sites

data_dir = "/Volumes/HDD/Data/ztd/"
df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl_filter.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13]))
site_set = set(df['Sta'])
# exit()

fig = pygmt.Figure()

fig.basemap(region="-75/-10/55/86", projection="L-42.5/30/35/25/3i", frame=["x20", "y10"])
fig.coast(shorelines=True, water="white")
# pygmt.makecpt(cmap="viridis", series=[df.iloc[:,-1].min(), df.iloc[:,-1].max()])
fig.plot(
    x=df.iloc[:,2], # lon
    y=df.iloc[:,1], # lat
    style="c0.15c",
    # color=df.iloc[:,-1],
    color="red",
    # cmap = True,
    pen="black"
)
fig.text(text=df.iloc[:,0].to_list(),x=df.iloc[:,2]+1,y=df.iloc[:,1]+0.1, justify="ML", font="8p")
# fig.text(text=df.iloc[:-3,0].to_list(),x=df.iloc[:-3,2]+1,y=df.iloc[:-3,1]+0.1, justify="ML", font="12p")
# fig.text(text=df.iloc[-3:,0].to_list(),x=df.iloc[-3:,2]-1.5,y=df.iloc[-3:,1]+1, justify="MC", font="12p")
# fig.colorbar(frame='af+l"End year"')
fig.savefig("figs/greenland_gps_pos_name.png")