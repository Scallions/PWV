import numpy as np



import pygmt
import pandas as pd
import sys
sys.path.append(".")
from data.filter_sites import greenland_sites
import xarray as xr

data_dir = "/Volumes/HDD/Data/ztd/gan/"
rps = np.load(data_dir + "rps.npy")
# print(rps.shape)
ds = xr.DataArray(rps, dims=("lat", "lon"), coords={
    "lon": np.linspace(-75,-12, rps.shape[1]),
	"lat": np.linspace(85,55, rps.shape[0]),
})
# print(ds)
# exit()

data_dir = "/Volumes/HDD/Data/ztd/"
df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl_filter.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13]))
site_set = set(df['Sta'])

fig = pygmt.Figure()

fig.basemap(region="-75/-12/55/85", projection="L-42.5/30/35/25/3i", frame=["x20", "y10"])
pygmt.makecpt(cmap="viridis", series=[rps.min(), rps.max()])
fig.grdimage(
    grid = ds,
    cmap = True,
)
fig.coast(shorelines=True)
fig.plot(
    x=df.iloc[:,2], # lon
    y=df.iloc[:,1], # lat
    style="c0.15c",
    # color=df.iloc[:,-1],
    # color="red",
    # cmap = True,
    # pen="black"
    pen = "red"
)
fig.colorbar(frame=['x0.1'])
fig.savefig("figs/greenland_rps.png")