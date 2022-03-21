"""
把meta不是格陵兰岛上的站去掉
"""

import os
import pandas as pd
from tqdm import tqdm


data_dir = "/Volumes/HDD/Data/ztd/"


df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13])
print(df.columns)
lon = df["Long(deg)"]
lat = df["Lat(deg)"]
df = df[(lon>360-75) & (lon<360-10) & (lat>55) & (lat<86)]


for row in tqdm(df.itertuples(), total=df.shape[0]):
    sitename = row[1]
    if os.path.exists(data_dir+f"mete_raw/{sitename}.csv"):
        os.rename(data_dir+f"mete_raw/{sitename}.csv", data_dir+f"mete/{sitename}.csv")
    elif os.path.exists(data_dir+f"meta_raw/{sitename.lower()}.csv"):
        os.rename(data_dir+f"mete_raw/{sitename.lower()}.csv", data_dir+f"mete_raw/{sitename}.csv")