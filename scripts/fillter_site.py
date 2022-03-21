"""
筛选数据较多的测站信息
"""

import pandas as pd

data_dir = "/Volumes/HDD/Data/ztd/"


df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13])

df2 = pd.read_csv("dataset/timespan_filter.csv")

ridx = df['Sta'].isin(df2['name'])

df3 = df[ridx]
df3.to_csv(data_dir+"gps_sites_1d_hz_grl_filter.csv", index=False)