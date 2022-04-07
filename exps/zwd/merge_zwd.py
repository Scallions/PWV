"""
生成zwd
"""

import pandas as pd
import glob
from datetime import date

data_dir = "/Volumes/HDD/Data/ztd/"
df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl_filter.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13]))
site_set = set(df['Sta'])
start = date(2010,1,2)
end = date(2022,1,30)
indexs = pd.date_range(start=start,end=end)
out_df = pd.DataFrame([], columns=list(site_set), index=indexs)
total = len(glob.glob(data_dir+"mete/*.csv"))
for fp in glob.iglob(data_dir+"mete/*.csv"):
    sitename = fp.split("/")[-1][:4]
    if sitename not in site_set:
        continue
    site_data = pd.read_csv(fp, parse_dates=['time'])
    site_data.set_index('time', inplace=True)
    out_df[sitename] = site_data['zwd']

out_df.to_csv(data_dir+"zwd_1d_hz_grl_filter.csv")
