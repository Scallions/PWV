"""
输出小时分辨率和era对应上
"""

import pandas as pd
import glob
from datetime import date, datetime

data_dir = "/Volumes/HDD/Data/ztd/"
df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl_filter.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13]))
site_set = set(df['Sta'])
start = datetime(2010,1,2,0)
end = datetime(2022,1,30,23)
indexs = pd.date_range(start=start,end=end, freq='H')
out_df = pd.DataFrame([], columns=list(site_set), index=indexs)
total = len(glob.glob(data_dir+"all/*.csv"))
for fp in glob.iglob(data_dir+"all/*.csv"):
    sitename = fp.split("/")[-1][:4]
    if sitename not in site_set:
        continue
    site_data = pd.read_csv(fp, parse_dates=['time'])
    site_data = site_data.drop('Unnamed: 0', axis=1)
    site_data.set_index('time', inplace=True)
    site_data = site_data.resample('H').mean()
    out_df[sitename] = site_data['pwv']

out_df.to_csv(data_dir+"pwv_1h_hz_grl_filter.csv")