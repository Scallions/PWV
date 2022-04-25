import numpy as np
import pygmt
import pandas as pd
import sys
sys.path.append(".")
from data.filter_sites import greenland_sites
import xarray as xr
import pickle
from datetime import datetime, timedelta

from data.tools import common_data
from model.dcgenerator import DCGenerator
import paddle

data_dir = "/Volumes/HDD/Data/ztd/"
fp = f"{data_dir}/pwv_1h_hz_grl_filter_miss.csv"
gps = pd.read_csv(fp, parse_dates=[0], index_col=[0])
era = xr.load_dataarray(f'{data_dir}/pwv.nc')
era_max = era.min(axis=0)[:31,:64]
era_min = era.max(axis=0)[:31,:64]
gps = gps[gps.isna().any(axis=1)==False]
gps, era = common_data(gps, era)
tidxs = gps.index
gps_m = 5.78
gps_s = 3.43
era_m = era.mean(axis=0)
era_s = era.std(axis=0)
# era_max = era.min(axis=0)
# era_min = era.max(axis=0)
gps = (gps-gps_m)/gps_s
# era = (era-era_m)/era_s

t = datetime(2010,9,1,12)
s = tidxs[0]
idx = int((t-s).total_seconds())//3600
print(idx, t)

def to_realscale(pwvs):
    return pwvs.detach().numpy()*(era_max-era_min)+era_min

gan = DCGenerator(35,1)
gan.set_state_dict(paddle.load(f"{data_dir}/G_last.pdmodel"))
gan.eval()
era = era.values[:,:31,:64]
gps = gps.values
# print(gps.shape, era.shape)

gp = gps[idx,:]
er = era[idx,:,:]
o = gan(paddle.to_tensor(gp.reshape([1,35]),dtype=paddle.float32))
# print(o.shape, era_min.shape)
pred = to_realscale(o[0,:,:])
# raw = to_realscale(paddle.to_tensor(er[:,:]))
raw = er
# print(pred.shape, raw.shape)
ds = xr.DataArray(pred, dims=("lat", "lon"), coords={
    "lon": np.linspace(-75,-12, pred.shape[1]),
	"lat": np.linspace(85,55, pred.shape[0]),
})
ds1 = xr.DataArray(raw, dims=("lat", "lon"), coords={
    "lon": np.linspace(-75,-12, raw.shape[1]),
	"lat": np.linspace(85,55, raw.shape[0]),
})



data_dir = "/Volumes/HDD/Data/ztd/"
df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl_filter.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13]))
site_set = set(df['Sta'])

pygmt.config(FONT_TITLE="12p")
pygmt.config(MAP_TITLE_OFFSET="-4p")
pygmt.config(FONT_HEADING="14p")
fig = pygmt.Figure()
cmap = "jet"
maxt = max(pred.max(), raw.max()).item()+1
# print(maxt)
maxt = 30
tstr = t.strftime("%Y%m%d-%H")

# figsize 宽高
with fig.subplot(nrows=1, ncols=2, figsize=("5i", "2.5i"), autolabel="(a)+o0c/-0.3c", margins=["0.1c", "0.1c"],title=tstr):
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
fig.savefig(f"figs/greenland_{tstr}.png")