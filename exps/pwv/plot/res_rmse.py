"""
残差rmse分布
"""

import pygmt
import pandas as pd
import sys
sys.path.append(".")
from data.filter_sites import greenland_sites

data_dir = "/Volumes/HDD/Data/ztd/"
df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl_filter.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13]))
site_set = set(df['Sta'])
rms = pd.read_csv(data_dir+"pwv_1d_res_grl.csv")

rms = rms.std()
# print(rms)
# exit()
print(rms.mean())

df = df.sort_values(by=['Sta'])
# trends = trends.sort_values(by=['site'])

# print(df.head())
# print(rms[df["Sta"]])
# # print(trends.head())
# exit()

# idxs = trends["trend"] != "no trend"
# print(idxs)

fig = pygmt.Figure()

fig.basemap(region="-75/-10/55/86", projection="L-42.5/30/35/25/3i", frame=["x20", "y10"])
fig.coast(shorelines=True, water="white")
pygmt.makecpt(cmap="seis", series=[rms.min(), rms.max()])
fig.plot(
    x=df.iloc[:,2], # lon
    y=df.iloc[:,1], # lat
    style="c0.15c",
    color=rms[df["Sta"]],
    # color="red",
    cmap = True,
    pen="black"
)
# fig.text(text=df.iloc[:,0].to_list(),x=df.iloc[:,2]+1,y=df.iloc[:,1]+0.1, justify="ML", font="8p")
# fig.text(text=df.iloc[:-3,0].to_list(),x=df.iloc[:-3,2]+1,y=df.iloc[:-3,1]+0.1, justify="ML", font="12p")
# fig.text(text=df.iloc[-3:,0].to_list(),x=df.iloc[-3:,2]-1.5,y=df.iloc[-3:,1]+1, justify="MC", font="12p")
fig.colorbar(frame='af+l"mm"')
fig.savefig("figs/greenland_res_rmse.png")