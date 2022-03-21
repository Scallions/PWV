"""
累积可降雨量
"""

import pandas as pd
import matplotlib.pyplot as plt


total = len(glob.glob(data_dir+"mete/*.csv"))
stats = []
for fp in tqdm(glob.iglob(data_dir+"mete/*.csv"), total=total):
    sitename = fp.split("/")[-1][:4]
    site_data = pd.read_csv(fp, parse_dates=['time'])
    ts = site_data['ztd']
    ts = ts - ts.mean()
    ts = ts.values
    if len(ts) < 365:
        continue
    start = site_data['time'][0]
    tindex = site_data['time'].map(lambda x: (x - start).days)

dfall = pd.read_csv("dataset/pwv_angle_abs.csv")



import pygmt

start = dfall['year'].min()
end = dfall['year'].max()
for year in range(start, end+1):
    df = dfall[dfall["year"] == year]
    fig = pygmt.Figure()
    fig.basemap(region="-75/-10/55/86", projection="L-40/30/35/25/3i", frame=["x20", "y10"])
    fig.coast(shorelines=True, water="white")
    pygmt.makecpt(cmap="jet", series=[df.iloc[:,6].min(), df.iloc[:,6].max()])
    pygmt.makecpt(cmap="jet", series=[-0.01, 0.01])
    fig.plot(
        x=df.iloc[:,1], # lon
        y=df.iloc[:,2], # lat
        style="c0.15c",
        color=df.iloc[:,6],
        # color="black",
        cmap = True,
        pen="black"
    )
    fig.colorbar(frame=['x'])
    fig.savefig(f"figs/greenland_linear_{year}.png")