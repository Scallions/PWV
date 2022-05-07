import pygmt
import pandas as pd
import sys
sys.path.append(".")

data_dir = "/Volumes/HDD/Data/ztd/"

data_dir = "/Volumes/HDD/Data/ztd/"
df = pd.read_csv(data_dir+"./gps_sites_select.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13]))
# site_set = set(df['Sta'])
site_set = set(df.iloc[:,0])
# exit()
print(df.shape)
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
# fig.text(text=df.iloc[:,0].to_list(),x=df.iloc[:,2]+1,y=df.iloc[:,1]+0.1, justify="ML", font="8p")
# fig.text(text=df.iloc[:-3,0].to_list(),x=df.iloc[:-3,2]+1,y=df.iloc[:-3,1]+0.1, justify="ML", font="12p")
# fig.text(text=df.iloc[-3:,0].to_list(),x=df.iloc[-3:,2]-1.5,y=df.iloc[-3:,1]+1, justify="MC", font="12p")
# fig.colorbar(frame='af+l"End year"')
fig.savefig("figs/greenland_gps_sites_ml.png")