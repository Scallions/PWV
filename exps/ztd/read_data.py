"""
读取所有ztd数据并保存
"""

import pandas as pd
import glob
from tqdm import tqdm
from datetime import date

data_dir = "/Volumes/HDD/Data/ztd/"

total = len(glob.glob(data_dir+"mete/*.csv"))
stats = []

df = pd.read_csv(data_dir+"./gps_sites_1d_hz_grl_filter.csv", sep=r",", engine='python', on_bad_lines='skip')#lambda badline: badline[:13]))
site_set = set(df['Sta'])
start = date(2010,1,2)
end = date(2022,1,30)
indexs = pd.date_range(start=start,end=end)
out_df = pd.DataFrame([], columns=list(site_set), index=indexs)

for fp in tqdm(glob.iglob(data_dir+"mete/*.csv"), total=total):
    sitename = fp.split("/")[-1][:4]
    if sitename not in site_set:
        continue
    site_data = pd.read_csv(fp, parse_dates=['time'])
    site_data.set_index('time', inplace=True)
    out_df[sitename] = site_data['ztd']

out_df.to_csv(data_dir+"ztd_1d_hz_grl_filter.csv")
