
import geopandas as gpd

data_dir = "/Volumes/HDD/Data/GRL/"
basin_file = "GRE_Basins_IMBIE2_v1.3.zip"

gdf = gpd.read_file(data_dir+basin_file)
print(gdf)

import pygmt


regions = ["NW", "CW", "SW", "SE", "NE", "NO"]
colors = ["RED", "BLUE", "GREEN", "CYAN", "YELLOW", "ORANGE"]

fig = pygmt.Figure()

fig.basemap(region="-75/-10/55/86", projection="L-42.5/30/35/25/3i", frame=["x20", "y10"])
for color, region in zip(colors,regions):
    data = gdf[gdf["SUBREGION1"] == region]
    fig.plot(data=data, pen=f"1p,{color}", label=region, color=color)
fig.coast(shorelines=True, water="white")
fig.legend()
fig.savefig("figs/greenland_basins.png")