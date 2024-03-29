"""
趋势检验结果图
"""

import pygmt
import pandas as pd
import sys
sys.path.append(".")
from data.filter_sites import greenland_sites

data_dir = "/Volumes/HDD/Data/ztd/"
df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl_filter.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13]))
site_set = set(df['Sta'])
trends = pd.read_csv("dataset/trend.csv")

df = df.sort_values(by=['Sta'])
trends = trends.sort_values(by=['site'])
print(df.head())
print(trends.head())
# exit()

idxs = trends["trend"] != "no trend"
# print(idxs)

fig = pygmt.Figure()

fig.basemap(region="-75/-10/55/86", projection="L-42.5/30/35/25/3i", frame=["x20", "y10"])
import geopandas as gpd
data_dir = "/Volumes/HDD/Data/GRL/"
basin_file = "GRE_Basins_IMBIE2_v1.3.zip"
gdf = gpd.read_file(data_dir+basin_file)
regions = ["NW", "CW", "SW", "SE", "NE", "NO"]
colors = ["RED", "BLUE", "GREEN", "CYAN", "YELLOW", "ORANGE"]
fig.basemap(region="-75/-10/55/86", projection="L-42.5/30/35/25/3i", frame=["x20", "y10"])
for color, region in zip(colors,regions):
    data = gdf[gdf["SUBREGION1"] == region]
    fig.plot(data=data, label=region, color=color)
fig.coast(shorelines=True, water="white")
fig.legend()
fig.coast(shorelines=True, water="white")
fig.plot(
    x=df.iloc[:,2], # lon
    y=df.iloc[:,1], # lat
    style="c0.15c",
    # color=trends[idxs]['slope'],
    # color="red",
    color="black",
    # cmap = True,
    pen="black"
)
pygmt.makecpt(cmap="seis", series=[trends['slope'].min(), trends['slope'].max()])
fig.plot(
    x=df[idxs.values].iloc[:,2], # lon
    y=df[idxs.values].iloc[:,1], # lat
    style="c0.15c",
    color=trends[idxs]['slope'],
    # color="red",
    cmap = True,
    pen="black"
)
# fig.text(text=df.iloc[:,0].to_list(),x=df.iloc[:,2]+1,y=df.iloc[:,1]+0.1, justify="ML", font="8p")
# fig.text(text=df.iloc[:-3,0].to_list(),x=df.iloc[:-3,2]+1,y=df.iloc[:-3,1]+0.1, justify="ML", font="12p")
# fig.text(text=df.iloc[-3:,0].to_list(),x=df.iloc[-3:,2]-1.5,y=df.iloc[-3:,1]+1, justify="MC", font="12p")
fig.colorbar(frame='af+l"mm/year"')
fig.savefig("figs/greenland_trends.png")