



import numpy as np


eras = np.load("/Volumes/SSD/Code/Workspace/paddle/GAN_RNN/eras.npy")[:,::-1,:]
outs = np.load("/Volumes/SSD/Code/Workspace/paddle/GAN_RNN/outs.npy")[:,::-1,:]


print(eras.shape)
import xarray as xr

import pygmt
pygmt.config(FONT_TITLE="12p")
pygmt.config(MAP_TITLE_OFFSET="-4p")
pygmt.config(FONT_HEADING="14p")
fig = pygmt.Figure()
cmap = "jet"
maxt = max(outs.max(), eras.max())+1
# maxt = 30

# figsize 宽高
with fig.subplot(nrows=4, ncols=3, figsize=("5i", "6.5i"), autolabel="(a)+o0c/-0.2c", margins=["0.1c", "0.1c"],title="2019-03-01"):
    for i in range(12):
        row = i // 3
        col = i % 3
        ds = xr.DataArray(eras[2*i,:,:], dims=("lat", "lon"), coords={
            "lon": np.linspace(-75,-12, eras.shape[2]),
            "lat": np.linspace(85,55, eras.shape[1]),
        })
        with fig.set_panel(panel=[row, col]):
            fig.basemap(region="-75/-12/55/85", projection="L-43.5/30/35/25/1i", frame=["x20", "y20", f"+t{2*i}:00"])
            pygmt.makecpt(cmap=cmap, series=[0, maxt])
            fig.grdimage(region="-75/-12/55/85", projection="L-43.5/30/35/25/1i",
                grid = ds,
                cmap = True,
            )
            fig.coast(region="-75/-12/55/85", projection="L-43.5/30/35/25/1i",shorelines=True)
            # fig.plot(region="-75/-12/55/85", projection="L-43.5/30/35/25/1i",
            #     x=df.iloc[:,2], # lon
            #     y=df.iloc[:,1], # lat
            #     style="c0.15c",
            #     # color=df.iloc[:,-1],
            #     # color="red",
            #     # cmap = True,
            #     # pen="black"
            #     pen = "red"
            # )
fig.colorbar(region="-75/-12/55/85", projection="L-43.5/30/35/25/1i",frame=True, position="+jCB+h+w6c+o0c/-1c")

fig.savefig(f"figs/greenland_daypred_era.png")

# figsize 宽高
with fig.subplot(nrows=4, ncols=3, figsize=("5i", "6.5i"), autolabel="(a)+o0c/-0.2c", margins=["0.1c", "0.1c"],title="2019-03-01"):
    for i in range(12):
        row = i // 3
        col = i % 3
        ds = xr.DataArray(outs[2*i,:,:], dims=("lat", "lon"), coords={
            "lon": np.linspace(-75,-12, eras.shape[2]),
            "lat": np.linspace(85,55, eras.shape[1]),
        })
        with fig.set_panel(panel=[row, col]):
            fig.basemap(region="-75/-12/55/85", projection="L-43.5/30/35/25/1i", frame=["x20", "y20", f"+t{2*i}:00"])
            pygmt.makecpt(cmap=cmap, series=[0, maxt])
            fig.grdimage(region="-75/-12/55/85", projection="L-43.5/30/35/25/1i",
                grid = ds,
                cmap = True,
            )
            fig.coast(region="-75/-12/55/85", projection="L-43.5/30/35/25/1i",shorelines=True)
            # fig.plot(region="-75/-12/55/85", projection="L-43.5/30/35/25/1i",
            #     x=df.iloc[:,2], # lon
            #     y=df.iloc[:,1], # lat
            #     style="c0.15c",
            #     # color=df.iloc[:,-1],
            #     # color="red",
            #     # cmap = True,
            #     # pen="black"
            #     pen = "red"
            # )
            # fig.colorbar(region="-75/-12/55/85", projection="L-43.5/30/35/25/1i",frame=['x10'])

fig.savefig(f"figs/greenland_daypred.png")