"""
生成三维层析的数据集
"""

import pandas as pd
import glob
from datetime import datetime

data_dir = "/Volumes/HDD/Data/ztd/"
df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl_filter.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13]))
site_set = set(df['Sta'])
start = datetime(2010,1,2,0)
end = datetime(2022,1,30,23)
colnames = []
for site in site_set:
    colnames.append(site+"_pwv")
    colnames.append(site+"_gn")
    colnames.append(site+"_ge")
indexs = pd.date_range(start=start,end=end, freq='H')
out_df = pd.DataFrame([], columns=colnames, index=indexs)
total = len(glob.glob(data_dir+"all_g/*.csv"))
for fp in glob.iglob(data_dir+"all_g/*.csv"):
    sitename = fp.split("/")[-1][:4]
    if sitename not in site_set:
        continue
    site_data = pd.read_csv(fp, parse_dates=['time'])
    site_data.set_index('time', inplace=True)
    site_data = site_data.resample('H').mean()
    out_df[sitename+"_pwv"] = site_data['pwv']
    out_df[sitename+"_gn"] = site_data['gn']
    out_df[sitename+"_ge"] = site_data['ge']

out_df.to_csv(data_dir+"pwv+g_1h_hz_grl_filter.csv")
