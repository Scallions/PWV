"""
线性趋势项
"""


import pandas as pd
import matplotlib.pyplot as plt


dfall = pd.read_csv("dataset/ztd_angle_abs.csv")
import pygmt

start = dfall['year'].min()
end = dfall['year'].max()
for year in range(start, end+1):
    df = dfall[dfall["year"] == year]
    fig = pygmt.Figure()
    fig.basemap(region="-75/-10/55/86", projection="L-42.5/30/35/25/3i", frame=["x20", "y10"])
    fig.coast(shorelines=True, water="white")
    # pygmt.makecpt(cmap="jet", series=[df.iloc[:,6].min(), df.iloc[:,6].max()])
    pygmt.makecpt(cmap="jet", series=[-0.2, 0.2])
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
    fig.savefig(f"figs/ztd_greenland_linear_{year}.png")