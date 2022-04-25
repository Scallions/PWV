import numpy as np
import pygmt
import pandas as pd
import sys
sys.path.append(".")
from data.filter_sites import greenland_sites
import xarray as xr
import pickle
from datetime import datetime, timedelta

data_dir = "/Volumes/HDD/Data/ztd/gan/"
preds = np.load(data_dir + "pred.npy")
eras = np.load(data_dir + "eras.npy")
with open(data_dir+'idxs_test1.pkl', 'rb') as f:
    idxs = pickle.load(f)
# idxs = pickle.load(data_dir+"idxs_test1.pkl")
print(idxs[:10])
print(preds.shape)

idx = 24*30*6 - 9 - 4*24 + 6*30*24
cmap = "jet"
start = datetime(2010,1,2)
date = datetime(2019,1,5,12)
hours = int((date-start).total_seconds()/3600)
idx = hours - idxs[0]
print("idx:", idx)
print(date)
dstr = date.strftime("%Y%m%d-%H")
print(f"{dstr}_pred")

pred = preds[idx,:,:]
era = eras[idx,:,:]
ds = xr.DataArray(pred, dims=("lat", "lon"), coords={
    "lon": np.linspace(-75,-12, preds.shape[2]),
	"lat": np.linspace(85,55, preds.shape[1]),
})
ds1 = xr.DataArray(era, dims=("lat", "lon"), coords={
    "lon": np.linspace(-75,-12, eras.shape[2]),
	"lat": np.linspace(85,55, eras.shape[1]),
})
# print(ds)
# exit()

data_dir = "/Volumes/HDD/Data/ztd/"
df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl_filter.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13]))
site_set = set(df['Sta'])

pygmt.config(FONT_TITLE="12p")
pygmt.config(MAP_TITLE_OFFSET="-4p")
pygmt.config(FONT_HEADING="14p")
fig = pygmt.Figure()

maxt = max(preds.max(), eras.max())+1
maxt = 30

# figsize 宽高
with fig.subplot(nrows=1, ncols=2, figsize=("5i", "2.5i"), autolabel="(a)+o0c/-0.3c", margins=["0.1c", "0.1c"],title=dstr):
    with fig.set_panel(panel=[0, 0]):
        fig.basemap(region="-75/-12/55/85", projection="L-43.5/30/35/25/2i", frame=["x20", "y10", "+tGPS-GEN"])
        pygmt.makecpt(cmap=cmap, series=[0, maxt])
        fig.grdimage(region="-75/-12/55/85", projection="L-43.5/30/35/25/2i",
            grid = ds,
            cmap = True,
        )
        fig.coast(region="-75/-12/55/85", projection="L-43.5/30/35/25/2i",shorelines=True)
        fig.plot(region="-75/-12/55/85", projection="L-43.5/30/35/25/2i",
            x=df.iloc[:,2], # lon
            y=df.iloc[:,1], # lat
            style="c0.15c",
            # color=df.iloc[:,-1],
            # color="red",
            # cmap = True,
            # pen="black"
            pen = "red"
        )
        fig.colorbar(region="-75/-12/55/85", projection="L-43.5/30/35/25/2i",frame=['x10'])

    with fig.set_panel(panel=[0, 1]):
        fig.basemap(region="-75/-12/55/85", projection="L-43.5/30/35/25/2i", frame=["x20", "y10", "+tERA"])
        pygmt.makecpt(cmap=cmap, series=[0, maxt])
        fig.grdimage(region="-75/-12/55/85", projection="L-43.5/30/35/25/2i",
            grid = ds1,
            cmap = True,
        )
        fig.coast(region="-75/-12/55/85", projection="L-43.5/30/35/25/2i",shorelines=True)
        fig.plot(region="-75/-12/55/85", projection="L-43.5/30/35/25/2i",
            x=df.iloc[:,2], # lon
            y=df.iloc[:,1], # lat
            style="c0.15c",
            # color=df.iloc[:,-1],
            # color="red",
            # cmap = True,
            # pen="black"
            pen = "red"
        )
        fig.colorbar(region="-75/-12/55/85", projection="L-43.5/30/35/25/2i",frame=['x10'])
fig.savefig(f"figs/greenland_{dstr}.png")