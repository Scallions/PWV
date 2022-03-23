"""
格网布局
"""

import pandas as pd
import matplotlib.pyplot as plt


dfall = pd.read_csv("dataset/pwv_angle_abs.csv")
import pygmt

pygmt.config(MAP_TITLE_OFFSET="1p")
pygmt.config(MAP_HEADING_OFFSET="1p")

start = dfall['year'].min()
end = dfall['year'].max()
fig = pygmt.Figure()
with fig.subplot(nrows = 4, ncols = 3, figsize=("20c", "30c"), autolabel="(a)+o0c/-0.3c", margins=["0.1c", "1c"]):
    for year in range(start, end+1):
        i = year -start
        row = i // 3
        col = i % 3
        df = dfall[dfall["year"] == year]

        # fig.shift_origin(yshift="h-1c")
        with fig.set_panel(panel=[row, col]):
            fig.basemap(region="-75/-10/55/86", projection="L-42.5/30/35/25/2i", frame=["x20", "y10", f"+t{year}"])
            fig.coast(region="-75/-10/55/86", projection="L-42.5/30/35/25/2i",shorelines=True, water="white")
            pygmt.makecpt(cmap="jet", series=[-0.01, 0.01])
            fig.plot(region="-75/-10/55/86", projection="L-42.5/30/35/25/2i",
                x=df.iloc[:,1], # lon
                y=df.iloc[:,2], # lat
                style="c0.2c",
                color=df.iloc[:,6],
                # color="black",
                cmap = True,
                pen="black"
            )
pygmt.makecpt(cmap="jet", series=[-0.01, 0.01])
fig.colorbar(position="+jLB+h+w6c+o5.8c/-1c", frame=['x'])
fig.savefig(f"figs/linear_grid.png")